# Exoplanets

A simple analysis of exoplanet data for [ASTR 2040](http://lasp.colorado.edu/~espoclass/ASTR_2040_Fall_2016.htm), the Search for Life in the Universe, at the University of Colorado Boulder.

This program is setup to run on data from the [NASA Exoplanet Archive](http://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=planets). When downloading the data be sure to include the options for 'all columns' and 'all rows'.

The only dependency to run is python 3.
```
$ python3 planets.py <your-data.csv> [-v for extra logging]
```

To do analysis on parameters other than the defaults, add them to the array towards the bottom of `planets.py` (sorry this should be possible from the command line, but who is really going to use this anyway? :see_no_evil:)

## License

MIT © Michael Guida
