"""Download public primary papers and extract text for the novelty audit."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import json
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent / "sources"
PAPERS = {
    "xu_chen_han_2025": "https://arxiv.org/pdf/2501.16223",
    "choi_kwon_liao_rank": "https://arxiv.org/pdf/2311.16440",
    "armstrong_weidner_zeleneev": "https://arxiv.org/pdf/2210.06639",
    "ke_song_zhao_wang_2026": "https://www3.stat.sinica.edu.tw/ss_newpaper/SS-2026-0222_na.pdf",
    "carpentier_klopp_loffler_nickl": "https://arxiv.org/pdf/1608.04861",
    "carpentier_nickl_detection": "https://arxiv.org/pdf/1507.03829",
    "xia_zhang_zhou": "https://arxiv.org/pdf/2012.14844",
    "cai_low_adaptation": "https://arxiv.org/pdf/math/0503662",
    "zhu_weak_factors": "https://arxiv.org/pdf/1910.10382",
    "xia_yuan_linear_forms": "https://arxiv.org/pdf/1909.00116",
    "cai_liang_rakhlin": "https://arxiv.org/pdf/1404.4408",
    "carpentier_eisert_gross_nickl": "https://arxiv.org/pdf/1504.03234",
    "carpentier_kim": "https://arxiv.org/pdf/1502.04654",
    "agterberg_zhang": "https://arxiv.org/pdf/2410.06381",
    "bykhovskaya_gorin_sodin": "https://arxiv.org/pdf/2507.18554",
    "drton_singularities": "https://arxiv.org/pdf/math/0703360",
    "kutschan_tt_cone": "https://arxiv.org/pdf/1705.10152",
    "gao_peng_yuan_tucker_cone": "https://arxiv.org/pdf/2311.18324",
}

def fetch(item):
    name, url = item
    try:
        path = ROOT / (name + ".pdf")
        if not path.exists():
            with urllib.request.urlopen(url, timeout=40) as response:
                data = response.read()
            if not data.startswith(b"%PDF"):
                raise ValueError("Response is not a PDF")
            path.write_bytes(data)
        reader = PdfReader(path)
        (ROOT / (name + ".txt")).write_text("\n".join(
            f"\n[PDF PAGE {i+1}]\n" + (p.extract_text() or "").replace("\x00", "")
            for i, p in enumerate(reader.pages)))
        return {"id": name, "url": url, "pages": len(reader.pages), "status": "downloaded and extracted"}
    except Exception as exc:
        return {"id": name, "url": url, "status": "failed", "error": str(exc)}

if __name__ == "__main__":
    ROOT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, PAPERS.items()))
    (ROOT / "download_manifest.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
