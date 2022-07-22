Nf = 200
fmin = 1 # 1/micron => 300 THz
fmax = 3 # 1/micron => 900 THz
fre = np.linspace(fmin, fmax, Nf)
fcen = (fmin+fmax)/2          # center frequency
df = (fmax-fmin)                  # frequency width
omega = 2 * np.pi * fre
sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df), component=mp.Ex, 
                     center=mp.Vector3(z=-2))]