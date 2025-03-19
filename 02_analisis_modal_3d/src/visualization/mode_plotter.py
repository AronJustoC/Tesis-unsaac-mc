# Visualizar los modos
for i in range(len(freqs)):
    plot_mode_shape(
        structure,
        modes[:, i],
        title=f"Modo {i + 1} - {freqs[i]:.2f} Hz",
        deformation_scale=100,
    )
