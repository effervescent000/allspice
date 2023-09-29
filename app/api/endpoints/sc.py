import os
import subprocess

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import SoundChangeRules, User
from app.schemas.requests import SCInput
from app.schemas.responses import SCOutput

router = APIRouter()


@router.post("/", response_model=SCOutput)
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
