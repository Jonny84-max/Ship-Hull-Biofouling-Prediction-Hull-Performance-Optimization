import numpy as np
import plotly.graph_objects as go

def hull_3d_figure():
    # Ship principal dimensions
    L = 160
    B = 24
    T = 9

    bow_len = 0.22 * L
    stern_len = 0.18 * L
    mid_len = L - bow_len - stern_len

    bulb_length = 0.12 * L
    bulb_radius = 0.35 * T

    # Computational grid
    x = np.linspace(0, L, 220)
    y = np.linspace(-B/2, B/2, 90)
    X, Y = np.meshgrid(x, y)
    Z = np.full_like(X, np.nan)

    def section_shape(yi):
        return np.sqrt(1 - (2 * yi / B) ** 2)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            xi = X[i, j]
            yi = Y[i, j]

            # Bow
            if xi <= bow_len:
                f = np.sin((xi / bow_len) * np.pi / 2)

            # Parallel mid-body
            elif xi <= bow_len + mid_len:
                f = 1.0

            # Stern
            else:
                xs = (L - xi) / stern_len
                f = np.sin(xs * np.pi / 2)

            section = section_shape(yi)
            if section < 0:
                continue

            z_hull = -T * f * section

            # Bulbous bow
            if xi <= bulb_length:
                bulb_shape = bulb_radius * np.sqrt(max(0, 1 - (xi / bulb_length) ** 2))
                if abs(yi) < bulb_radius:
                    z_hull -= bulb_shape * np.sqrt(max(0, 1 - (yi / bulb_radius) ** 2))

            Z[i, j] = z_hull

    # Plot
    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Blues',
        opacity=0.9,
        showscale=False
    ))

    # Waterline (z=0)
    fig.add_trace(go.Scatter3d(
        x=x, y=np.zeros_like(x), z=np.zeros_like(x),
        mode='lines',
        line=dict(color='cyan', width=4),
        name="Waterline"
    ))

    # Keel line (z = -T)
    fig.add_trace(go.Scatter3d(
        x=x, y=np.zeros_like(x), z=-T*np.ones_like(x),
        mode='lines',
        line=dict(color='black', width=4),
        name="Keel"
    ))

    # Deck line (z = 0.1*T)
    fig.add_trace(go.Scatter3d(
        x=x, y=np.zeros_like(x), z=0.1*T*np.ones_like(x),
        mode='lines',
        line=dict(color='white', width=4),
        name="Deckline"
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Length (m)"),
            yaxis=dict(title="Beam (m)"),
            zaxis=dict(title="Draft (m)"),
            aspectmode='manual',
            aspectratio=dict(x=2.5, y=0.8, z=0.6),
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig
