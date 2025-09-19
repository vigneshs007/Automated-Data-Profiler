cat > profiler.py <<'EOF'
#!/usr/bin/env python3
"""
Simple data profiler.
Usage:
  python profiler.py --input data.csv --outdir results
"""
import os, json, argparse, shutil
from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_csv(path, nrows=None):
    return pd.read_csv(path, nrows=nrows)

def summarize_df(df, top_n=5):
    summary = {"shape": list(df.shape), "columns": []}
    for col in df.columns:
        s = df[col]
        info = {
            "name": col,
            "dtype": str(s.dtype),
            "n_missing": int(s.isna().sum()),
            "pct_missing": float(s.isna().mean())
        }
        if pd.api.types.is_numeric_dtype(s):
            nonnull = s.dropna()
            if nonnull.empty:
                info.update({"count": 0, "mean": None, "std": None, "min": None, "max": None})
            else:
                info.update({
                    "count": int(nonnull.count()),
                    "mean": float(nonnull.mean()),
                    "std": float(nonnull.std()),
                    "min": float(nonnull.min()),
                    "max": float(nonnull.max())
                })
        else:
            vc = s.dropna().astype(str).value_counts()
            info["top"] = vc.head(top_n).to_dict()
        summary["columns"].append(info)
    return summary

def save_json(summary, outpath):
    os.makedirs(os.path.dirname(outpath) or ".", exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

def save_plots(df, outdir, max_cat=10) -> List[str]:
    os.makedirs(outdir, exist_ok=True)
    imgs = []
    # numeric histograms
    for col in df.select_dtypes(include=[np.number]).columns:
        plt.figure(figsize=(6,4))
        df[col].dropna().hist(bins=30)
        plt.title(col)
        plt.tight_layout()
        path = os.path.join(outdir, f"{col}_hist.png")
        plt.savefig(path)
        plt.close()
        imgs.append(path)
    # categorical bars
    for col in df.select_dtypes(exclude=[np.number]).columns:
        vc = df[col].dropna().astype(str).value_counts().head(max_cat)
        if vc.empty:
            continue
        plt.figure(figsize=(6,4))
        vc.plot(kind="bar")
        plt.title(col)
        plt.tight_layout()
        path = os.path.join(outdir, f"{col}_bar.png")
        plt.savefig(path)
        plt.close()
        imgs.append(path)
    return imgs

def generate_html_report(summary_json_path, imgs, out_html):
    with open(summary_json_path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    html = ["<html><head><meta charset='utf-8'><title>Profile report</title></head><body>"]
    html.append(f"<h1>Dataset shape: {summary.get('shape')}</h1>")
    html.append("<h2>Columns</h2><ul>")
    for c in summary.get("columns", []):
        html.append(f"<li><strong>{c['name']}</strong> (dtype: {c['dtype']}) — missing: {c['n_missing']} ({c['pct_missing']:.2%})</li>")
    html.append("</ul><h2>Plots</h2>")
    outdir = os.path.dirname(out_html) or "."
    for img in imgs:
        html.append(f"<div><img src='{os.path.basename(img)}' style='max-width:700px'></div>")
    html.append("</body></html>")
    os.makedirs(outdir, exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    # copy images next to the html
    for img in imgs:
        try:
            shutil.copy(img, os.path.join(outdir, os.path.basename(img)))
        except Exception:
            pass

def main():
    p = argparse.ArgumentParser(description="Simple data profiler")
    p.add_argument("--input", "-i", required=True, help="CSV input file")
    p.add_argument("--outdir", "-o", default="results", help="Output folder")
    p.add_argument("--nrows", type=int, default=None, help="Read only nrows")
    args = p.parse_args()
    df = read_csv(args.input, nrows=args.nrows)
    os.makedirs(args.outdir, exist_ok=True)
    summary = summarize_df(df)
    summary_path = os.path.join(args.outdir, "summary.json")
    save_json(summary, summary_path)
    imgs = save_plots(df, os.path.join(args.outdir, "images"))
    html_path = os.path.join(args.outdir, "report.html")
    generate_html_report(summary_path, imgs, html_path)
    print("Report saved:", html_path)

if __name__ == "__main__":
    main()
EOF
