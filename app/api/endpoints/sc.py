from fastapi import APIRouter

router = APIRouter()


# @router.post("/", response_model=SCOutput)
# async def sca(
#     input: SCInput,
#     # current_user: User = Depends(deps.get_current_user),
# ):
#     word_list = open("input.wli", "w")
#     word_list.write("\n".join(input.word_list))
#     word_list.close()

#     sound_changes = open("sc.lsc", "w")
#     sound_changes.write(input.sound_changes)
#     sound_changes.close()

#     path = os.getcwd()
#     subprocess.run(
#         [f"{path}/app/core/lexurgy/bin/lexurgy", "sc", "sc.lsc", "input.wli"]
#     )
