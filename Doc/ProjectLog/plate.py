from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

import daft

# Instantiate the PGM.
pgm = daft.PGM([7.3, 4.3], origin=[-0.8, 0.3])

# Hierarchical parameters.
#pgm.add_node(daft.Node("alpha", r"$\alpha$", 0.5, 2, fixed=True))
#pgm.add_node(daft.Node("beta", r"$\beta$", 1.5, 2))

# Latent variable.
pgm.add_node(daft.Node("c", r"$c$", -0.4, 1.8, plot_params={"ec": "none"}))
pgm.add_node(daft.Node("b0", r"$B_0(\cdot)$", -0.4, 2.8, plot_params={"ec": "none"}))


pgm.add_node(daft.Node("w", r"$w_k$", 0.4, 1.8))
pgm.add_node(daft.Node("t", r"$\theta_k$", 0.4, 2.8))

#R,O
pgm.add_node(daft.Node("r", r"$R,O$", 1.3, 2.6))
#pgm.add_node(daft.Node("oo", r"$O$", 1.3, 2))

pgm.add_node(daft.Node("o", r"$\lambda$", 4.3, 0.8, plot_params={"ec": "none"}))

#f pi gamma
pgm.add_node(daft.Node("f", r"$f_i$", 2.3, 1.8))
pgm.add_node(daft.Node("p", r"$\pi_i$", 3.3, 1.8))
pgm.add_node(daft.Node("g", r"$\eta_i$", 4.3, 1.8))

pgm.add_node(daft.Node("z1", r"$z_1$", 2.3, 2.8))
pgm.add_node(daft.Node("z2", r"$z_2$", 3.3, 2.8))
pgm.add_node(daft.Node("zz3", r"$\cdots$", 3.8, 2.8, plot_params={"ec": "none"}))
pgm.add_node(daft.Node("z3", r"$z_3$", 4.3, 2.8))
pgm.add_node(daft.Node("z4", r"$z_4$", 5.3, 2.8))


pgm.add_node(daft.Node("y1", r"$y_1$", 2.3, 3.8,observed=True))
pgm.add_node(daft.Node("y2", r"$y_2$", 3.3, 3.8,observed=True))
pgm.add_node(daft.Node("yy3", r"$\cdots$", 3.8, 3.8, plot_params={"ec": "none"}))
pgm.add_node(daft.Node("y3", r"$y_3$", 4.3, 3.8,observed=True))
pgm.add_node(daft.Node("y4", r"$y_4$", 5.3, 3.8,observed=True))

pgm.add_edge("p", "z1")
pgm.add_edge("p", "z2")
pgm.add_edge("p", "z3")
pgm.add_edge("p", "z4")

pgm.add_edge("t", "y1")
pgm.add_edge("t", "y2")
pgm.add_edge("t", "y3")
pgm.add_edge("t", "y4")

pgm.add_edge("z1", "z2")
pgm.add_edge("z3", "z4")

pgm.add_edge("z1", "y1")
pgm.add_edge("z2", "y2")
pgm.add_edge("z3", "y3")
pgm.add_edge("z4", "y4")

pgm.add_edge("t","r")

pgm.add_edge("r", "p")

pgm.add_edge("o", "g")

pgm.add_edge("c", "w")
pgm.add_edge("b0", "t")
pgm.add_edge("c", "t")

pgm.add_edge("g", "p")
pgm.add_edge("f", "p")
pgm.add_edge("w", "f")
# And a plate.
pgm.add_plate(daft.Plate([-0.1, 1.3, 1, 2.1], label=r"{\footnotesize{ $k = 1,\ldots,\infty$}}", shift=-0.1))
pgm.add_plate(daft.Plate([1.75, 1.3, 4, 3], label=r"{\footnotesize{ $i = 1,\ldots,N$}}", shift=-0.1))

# Render and save.
pgm.render()
pgm.figure.savefig("classic.pdf")
#pgm.figure.savefig("classic.png", dpi=150)
