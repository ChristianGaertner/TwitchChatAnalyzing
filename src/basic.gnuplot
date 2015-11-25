set terminal png size 1350, 450

set output output

set grid

set xdata time

set timefmt "%s"

set xtics format "%H:%M"

plot input using 1:2 title chart_title with lines