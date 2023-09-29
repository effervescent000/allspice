import os
import subprocess

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Language, SoundChangeRules, User
from app.schemas.requests import SCInput, SoundChangeRulesRequest
from app.schemas.responses import SCOutput, SoundChangeRulesResponse
from app.utils.db_utils import verify_ownership

router = APIRouter()


@router.post("/apply", response_model=SCOutput)
async def sca(
    input: list[SCInput],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    output = []
    for x in input:
        word_list = open("input.wli", "w")
        word_list.write("\n".join(x.word_list))
        word_list.close()

        sound_change_rules = (
            await session.scalars(
                select(SoundChangeRules).where(
                    SoundChangeRules.id == x.sound_changes_id
                )
            )
        ).first()
        sc_file = open("sc.lsc", "w")
        sc_file.write(sound_change_rules.content)
        sc_file.close()

        path = os.getcwd()
        with subprocess.Popen(
            [f"{path}/app/core/lexurgy/bin/lexurgy", "sc", "sc.lsc", "input.wli"],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as p:
            for line in p.stdout:
                if "Wrote the final forms" in line:
                    p.terminate()

        out_file = open("input_ev.wli")
        output.extend(out_file.read().splitlines())
        out_file.close()
    return {"output": output}


@router.post("/", response_model=list[SoundChangeRulesResponse])
async def upsert_sound_changes(
    sound_change_rules: list[SoundChangeRulesRequest],
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    await verify_ownership(
        session,
        current_user=current_user,
        schema=SoundChangeRules,
        target_ids=[x.id for x in sound_change_rules if x.id is not None],
    )

    upserted = []
    for ruleset in sound_change_rules:
        new = await session.merge(SoundChangeRules(**ruleset.model_dump()))
        upserted.append(new)
    await session.commit()
    return upserted


@router.get("/", response_model=list[SoundChangeRulesResponse])
async def read_sound_changes(
    role: str | None = None,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    stmnt = select(SoundChangeRules)
    if role:
        stmnt = stmnt.where(SoundChangeRules.role == role)
    stmnt = stmnt.where(Language.user_id == current_user.id).join(Language)

    sc = (await session.scalars(stmnt)).unique().all()
    return sc
