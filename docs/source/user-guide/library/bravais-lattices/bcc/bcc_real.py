import radtools as rad

l = rad.lattice_example("BCC")
backend = rad.PlotlyBackend()
backend.plot(l, kind="primitive", label="primitive")
backend.plot(l, kind="conventional", label="conventional", color="black")
# Save an image:
backend.save("bcc_real.png")
# Interactive plot:
backend.show()
