import numpy as np
import plotly.graph_objects as go

def hull_fouled_figure(t=0.7):
    L = 160
    B = 24
    T = 9

    bow_len = 0.22 * L
    stern_len = 0.18 * L
    mid_len = L - bow_len - stern_len
    bulb_length = 0.12 * L
    bulb_radius = 0.35 * T

    x = np.linspace(0, L, 220)
    y = np.linspace(-B/2, B/2, 90)
    X, Y = np.meshgrid(x, y)
    Z_clean = np.full_like(X, np.nan)

    def section_shape(yi):
        return np.sqrt(1 - (2 * yi / B) ** 2)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            xi = X[i, j]
            yi = Y[i, j]

            if xi <= bow_len:
                f = np.sin((xi / bow_len) * np.pi / 2)
            elif xi <= bow_len + mid_len:
                f = 1.0
            else:
                xs = (L - xi) / stern_len
                f = np.sin(xs * np.pi / 2)

            section = section_shape(yi)
            if section < 0:
                continue

            z_hull = -T * f * section

            if xi <= bulb_length:
                bulb_shape = bulb_radius * np.sqrt(max(0, 1 - (xi / bulb_length) ** 2))
                if abs(yi) < bulb_radius:
                    z_hull -= bulb_shape * np.sqrt(max(0, 1 - (yi / bulb_radius) ** 2))

            Z_clean[i, j] = z_hull

    # Fouling
    np.random.seed(3)
    base_noise = 0.04 * np.random.randn(*X.shape)

    def fouling_growth(t):
        bow_effect = np.exp(-((X / L) * 4))
        return t * bow_effect * (0.2 * np.sin(5 * np.pi * X / L) + base_noise)

    Z_fouled = Z_clean - fouling_growth(t)

    fig = go.Figure()
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z_fouled,
        colorscale='Inferno',
        opacity=0.9,
        showscale=False,
        name="Fouled Hull"
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Length (m)"),
            yaxis=dict(title="Beam (m)"),
            zaxis=dict(title="Draft (m)")
        ),
        title="Fouled Ship Hull (Simulated)"
    )

    return fig
