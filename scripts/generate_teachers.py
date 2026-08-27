#!/usr/bin/env python3
"""Fictional teacher headshots via the local RealVisXL V5.0 + Compel stack on GPU 1 (3090).

No cpu_offload — Compel + offload = device mismatch (beautyfi lesson).
CUDA_VISIBLE_DEVICES must be the 3090, not the 6GB P106.
Skip files that already exist unless --force.
"""
import argparse
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # CUDA 0 = 3090 (nvidia-smi order is inverted)

import time
from pathlib import Path

import torch
from compel import Compel, ReturnedEmbeddingsType
from diffusers import StableDiffusionXLPipeline
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "assets" / "teachers"
OUT.mkdir(parents=True, exist_ok=True)

NEG = (
    "cartoon, illustration, painting, cgi, 3d render, wax, plastic skin, "
    "deformed face, extra fingers, text, watermark, logo, celebrity, "
    "nsfw, child, teen, underage"
)

# Square ID-photo vibe, like Dan's teacher tiles. Fictional adults only.
TEACHERS = [
    # --- Hilltop ---
    dict(id="sd1", seed=101, prompt=(
        "passport-style square photograph of a Polish woman in her mid-40s, "
        "kind dark-brown eyes, shoulder-length brown hair with a few grey strands, "
        "soft knit sweater, standing in a sunlit school corridor, "
        "photorealistic skin, 85mm, shallow depth of field, natural window light, "
        "looking at camera, slight smile, no makeup glam, no jewelry"
    )),
    dict(id="sd2", seed=202, prompt=(
        "passport-style square photograph of a Polish man in his early 40s, "
        "short dark hair, light stubble, round glasses, navy shirt, "
        "classroom blackboard softly blurred behind, photorealistic, 85mm, "
        "natural light, calm expression, looking at camera"
    )),
    dict(id="sd3", seed=303, prompt=(
        "passport-style square photograph of a Polish woman in her mid-30s, "
        "auburn hair in a low ponytail, green cardigan, lab-coat hint, "
        "science classroom shelves blurred, photorealistic, 85mm, "
        "daylight, friendly, looking at camera"
    )),
    dict(id="sd4", seed=404, prompt=(
        "passport-style square photograph of a Polish man in his mid-50s, "
        "grey-brown hair, trimmed beard, tweed jacket, "
        "history classroom maps blurred behind, photorealistic, 85mm, "
        "window light, thoughtful, looking at camera"
    )),
    dict(id="sd5", seed=505, prompt=(
        "passport-style square photograph of a Polish woman in her early 30s, "
        "black hair with a paint-speck on the temple, denim shirt, "
        "art room easels blurred, photorealistic, 85mm, "
        "soft daylight, bright eyes, looking at camera"
    )),
    dict(id="sd6", seed=606, prompt=(
        "passport-style square photograph of a Polish man in his mid-30s, "
        "short blond hair, athletic, grey polo shirt, "
        "school gymnasium blurred behind, photorealistic, 85mm, "
        "overhead lights, easy smile, looking at camera"
    )),
    # --- Grove (Leśna Polana) ---
    dict(id="gv1", seed=701, prompt=(
        "passport-style square photograph of a Polish woman in her late 30s, "
        "warm brown eyes, wavy chestnut hair, cream blouse, "
        "primary-school library shelves blurred, photorealistic, 85mm, "
        "soft daylight, gentle smile, looking at camera"
    )),
    dict(id="gv2", seed=702, prompt=(
        "passport-style square photograph of a Polish man in his mid-40s, "
        "short salt-and-pepper hair, thin wire glasses, forest-green sweater, "
        "math classroom whiteboard blurred, photorealistic, 85mm, "
        "natural light, calm, looking at camera"
    )),
    dict(id="gv3", seed=703, prompt=(
        "passport-style square photograph of a Polish woman in her early 40s, "
        "light brown hair pinned back, freckles, moss-green cardigan, "
        "nature classroom plants blurred, photorealistic, 85mm, "
        "window light, friendly, looking at camera"
    )),
    dict(id="gv4", seed=704, prompt=(
        "passport-style square photograph of a Polish man in his early 30s, "
        "short dark hair, athletic build, olive sports polo, "
        "school sports hall blurred, photorealistic, 85mm, "
        "overhead lights, easy smile, looking at camera"
    )),
    # --- River ---
    dict(id="rv1", seed=801, prompt=(
        "passport-style square photograph of a Polish woman in her mid-40s, "
        "ash-blonde hair in a bob, sharp blue eyes, charcoal blazer, "
        "lyceum corridor windows blurred, photorealistic, 85mm, "
        "daylight, composed smile, looking at camera"
    )),
    dict(id="rv2", seed=802, prompt=(
        "passport-style square photograph of a Polish man in his late 40s, "
        "receding dark hair, neat beard, blue Oxford shirt, "
        "math classroom desks blurred, photorealistic, 85mm, "
        "window light, serious calm, looking at camera"
    )),
    dict(id="rv3", seed=803, prompt=(
        "passport-style square photograph of a Polish woman in her early 30s, "
        "long dark hair, hazel eyes, teal blouse, "
        "biology lab glassware blurred, photorealistic, 85mm, "
        "soft daylight, bright expression, looking at camera"
    )),
    dict(id="rv4", seed=804, prompt=(
        "passport-style square photograph of a Polish man in his mid-50s, "
        "grey hair, reading glasses on forehead, brown corduroy jacket, "
        "history room bookshelves blurred, photorealistic, 85mm, "
        "warm light, thoughtful, looking at camera"
    )),
    dict(id="rv5", seed=805, prompt=(
        "passport-style square photograph of a Polish woman in her late 20s, "
        "short copper hair, freckles, sky-blue sweater, "
        "language classroom posters blurred, photorealistic, 85mm, "
        "daylight, cheerful, looking at camera"
    )),
    # --- Dune ---
    dict(id="dn1", seed=901, prompt=(
        "passport-style square photograph of a Polish woman in her mid-30s, "
        "honey-blonde hair in a braid, sun-kissed skin, linen shirt, "
        "bright classroom by sandy light, photorealistic, 85mm, "
        "looking at camera, soft smile"
    )),
    dict(id="dn2", seed=902, prompt=(
        "passport-style square photograph of a Polish man in his early 40s, "
        "cropped sandy hair, light stubble, beige henley, "
        "classroom with coastal light, photorealistic, 85mm, "
        "calm, looking at camera"
    )),
    dict(id="dn3", seed=903, prompt=(
        "passport-style square photograph of a Polish woman in her late 20s, "
        "wavy black hair, silver hoop earring, white artist smock, "
        "art room with sea-light, photorealistic, 85mm, "
        "bright eyes, looking at camera"
    )),
    dict(id="dn4", seed=904, prompt=(
        "passport-style square photograph of a Polish man in his mid-30s, "
        "buzz cut, tanned, navy tracksuit top, "
        "outdoor sports court blurred, photorealistic, 85mm, "
        "easy grin, looking at camera"
    )),
    # --- Sun vocational ---
    dict(id="su1", seed=1001, prompt=(
        "passport-style square photograph of a Polish man in his mid-40s, "
        "short dark hair, safety glasses on head, charcoal work shirt, "
        "electronics workshop benches blurred, photorealistic, 85mm, "
        "workshop light, confident, looking at camera"
    )),
    dict(id="su2", seed=1002, prompt=(
        "passport-style square photograph of a Polish woman in her late 30s, "
        "hair in a practical bun, clear-eyed, denim work shirt, "
        "welding booth soft-focus behind, photorealistic, 85mm, "
        "industrial light, steady smile, looking at camera"
    )),
    dict(id="su3", seed=1003, prompt=(
        "passport-style square photograph of a Polish man in his early 50s, "
        "grey crew cut, strong jaw, dark polo with grease-smudge hint, "
        "auto shop lifts blurred, photorealistic, 85mm, "
        "overhead lights, wry smile, looking at camera"
    )),
    dict(id="su4", seed=1004, prompt=(
        "passport-style square photograph of a Polish woman in her early 30s, "
        "short black hair, sharp eyes, indigo button-up, "
        "electrical training board blurred, photorealistic, 85mm, "
        "cool fluorescent light, focused calm, looking at camera"
    )),
    # --- Star ---
    dict(id="st1", seed=1101, prompt=(
        "passport-style square photograph of a Polish woman in her mid-40s, "
        "silver-streaked dark hair, pale skin, soft grey sweater, "
        "winter-lit classroom, photorealistic, 85mm, "
        "cool daylight, warm smile, looking at camera"
    )),
    dict(id="st2", seed=1102, prompt=(
        "passport-style square photograph of a Polish man in his late 30s, "
        "reddish-brown hair, beard trimmed short, maroon flannel, "
        "math classroom chalkboard blurred, photorealistic, 85mm, "
        "northern light, calm, looking at camera"
    )),
    dict(id="st3", seed=1103, prompt=(
        "passport-style square photograph of a Polish woman in her early 30s, "
        "blonde hair in a loose knot, bright eyes, plum blouse, "
        "music room piano blurred, photorealistic, 85mm, "
        "soft daylight, lively smile, looking at camera"
    )),
    dict(id="st4", seed=1104, prompt=(
        "passport-style square photograph of a Polish man in his mid-30s, "
        "close-cropped dark hair, athletic, charcoal hoodie, "
        "indoor ice-rink soft-focus behind, photorealistic, 85mm, "
        "cool light, slight smile, looking at camera"
    )),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", nargs="*", help="Limit to these ids, e.g. gv1 gv2")
    args = ap.parse_args()

    todo = TEACHERS
    if args.only:
        want = set(args.only)
        todo = [t for t in TEACHERS if t["id"] in want]
    if not args.force:
        todo = [t for t in todo if not (OUT / f"{t['id']}.webp").exists()]
    if not todo:
        print("nothing to generate")
        return

    assert torch.cuda.is_available(), "CUDA required"
    print("GPU:", torch.cuda.get_device_name(0),
          f"{torch.cuda.get_device_properties(0).total_memory/1024**3:.1f} GB")
    print(f"generating {len(todo)} portraits → {OUT}")

    t0 = time.time()
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "SG161222/RealVisXL_V5.0",
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )
    pipe.to("cuda")
    pipe.enable_vae_slicing()
    compel = Compel(
        tokenizer=[pipe.tokenizer, pipe.tokenizer_2],
        text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
        returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
        requires_pooled=[False, True],
        device="cuda",
    )
    print(f"loaded in {time.time()-t0:.1f}s")

    for i, t in enumerate(todo, 1):
        dest = OUT / f"{t['id']}.webp"
        print(f"[{i}/{len(todo)}] {t['id']}")
        cond, pooled = compel(t["prompt"])
        ncond, npooled = compel(NEG)
        gen = torch.Generator(device="cuda").manual_seed(t["seed"])
        img = pipe(
            prompt_embeds=cond,
            pooled_prompt_embeds=pooled,
            negative_prompt_embeds=ncond,
            negative_pooled_prompt_embeds=npooled,
            width=1024,
            height=1024,
            num_inference_steps=28,
            guidance_scale=7.0,
            generator=gen,
        ).images[0]
        img = img.convert("RGB").resize((512, 512), Image.Resampling.LANCZOS)
        img.save(dest, "WEBP", quality=86)
        print("  ->", dest, dest.stat().st_size)


if __name__ == "__main__":
    main()
