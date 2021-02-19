freq="2412 2437 2462 5180 5200 5220 5240 5260 5280 5320"

while true; do
    for f in $freq; do 
	iw dev mon0  set freq $f
	echo $f
	sleep 0.5
    done
done

