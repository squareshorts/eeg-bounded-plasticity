#!/usr/bin/env python3
"""Render the primary bounded-residual architecture schematic (PDF/SVG/PNG).

Layout is sized for legible text at an Elsevier single-column preprint figure width.
The computational architecture and 2% source-probe constraint are unchanged.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 13.5,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
})

INK = '#20232A'
BLUE = '#2F6484'
GRAY = '#F1F3F4'
TINT = '#EAF3F8'


def box(ax, x, y, width, height, label, fill='#FFFFFF', edge=INK,
        font_size=13.0, weight='normal'):
    ax.add_patch(FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle='round,pad=0.03,rounding_size=0.08',
        facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=3,
    ))
    ax.text(x, y, label, ha='center', va='center', fontsize=font_size,
            color=INK, fontweight=weight, linespacing=1.13, zorder=4)


def arrow(ax, x0, y0, x1, y1, color=INK, dashed=False):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=14,
        linewidth=1.5, color=color, zorder=2,
        linestyle=(0,(4,3)) if dashed else '-',
    ))


def main():
    out = Path(__file__).resolve().parent / 'figures'
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11.6,4.2), dpi=220)
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0.2, 4.1)
    ax.axis('off')

    # Encoder and classifier stay unchanged; only the low-rank branch adapts.
    y = 1.45
    box(ax, 0.90, y, 1.50, 0.93, 'EEG bandpower\nfeatures')
    box(ax, 2.75, y, 1.75, 0.93, 'Frozen source\nencoder', GRAY)
    box(ax, 4.31, y, 0.77, 0.93, 'Latent\n$z$', font_size=13.4)
    box(ax, 6.28, y, 1.49, 0.93, 'Adapted latent\n' + r'$z^\prime=z+\Delta z$', font_size=12.5)
    box(ax, 8.21, y, 1.76, 0.93, 'Frozen source\nclassifier', GRAY)
    box(ax, 10.31, y, 1.77, 0.93, 'Class\nprobabilities')

    for start,end in [(1.65,1.875),(3.625,3.925),(4.705,5.075),
                      (5.365,5.535),(7.025,7.33),(9.09,9.425)]:
        arrow(ax,start,y,end,y)
    ax.add_patch(Circle((5.22,y),radius=0.14,facecolor='white',edgecolor=BLUE,
                        linewidth=1.8,zorder=5))
    ax.text(5.22,y,'+',fontsize=16,ha='center',va='center',color=BLUE,zorder=6)

    # Low-rank residual and its deterministic source-probe constraint.
    box(ax, 5.30, 3.23, 3.22, 0.95,
        'Rank-2 residual adapter\n' + r'$\Delta z=U\,\mathrm{GELU}(Vz)$',
        fill=TINT, edge=BLUE, font_size=13.2)
    box(ax, 9.32, 3.23, 3.65, 0.95,
        'Source-probe displacement\n' + r'projection: mean $D\leq2\%$',
        fill='#FCFCFC',edge=BLUE,font_size=12.0)
    arrow(ax, 4.31, 1.93, 4.50, 2.75, color=BLUE)
    arrow(ax, 5.30, 2.75, 5.22, 1.60, color=BLUE)
    arrow(ax, 7.47, 3.23, 6.95, 3.23, color=BLUE, dashed=True)

    fig.subplots_adjust(left=0.02,right=0.98,bottom=0.05,top=0.95)
    basename=out/'bounded_residual_architecture'
    fig.savefig(basename.with_suffix('.pdf'),bbox_inches='tight',pad_inches=0.08)
    fig.savefig(basename.with_suffix('.svg'),bbox_inches='tight',pad_inches=0.08)
    fig.savefig(basename.with_suffix('.png'),dpi=450,bbox_inches='tight',pad_inches=0.08)
    plt.close(fig)
    print(f'Exported vector and raster architecture figure to {basename}')


if __name__=='__main__':
    main()
