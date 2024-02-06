# 5e-10 sec per frame
fuv=udf/fuv-equiv.ovf
dir=orbits-0.51.out
csv=orbits-0.51.csv
mkdir $dir
rm $dir/*.png
for i in {1..180}; do
	echo "Processing "$csv"/"$i"..."
	python orbit2png.py $fuv $csv $i 2
	mv vf-1.png $dir/$i.png 
done

dir=orbits-1.39.out
csv=orbits-1.39.csv
mkdir $dir
rm $dir/*.png
for i in {1..90}; do
	echo "Processing "$csv"/"$i"..."
	python orbit2png.py $fuv $csv $i 1
	mv vf-1.png $dir/$i.png 
done

dir=orbits-2.10.out
csv=orbits-2.10.csv
mkdir $dir
rm $dir/*.png
for i in {1..50}; do
	echo "Processing "$csv"/"$i"..."
	python orbit2png.py $fuv $csv $i 1
	mv vf-1.png $dir/$i.png 
done



for dir in orbits-0.51.out orbits-1.39.out orbits-2.10.out; do
	shape=`echo $dir | awk '{sub(/^.*\//,""); sub(/.out$/,""); print $0}'`
	cd $dir
	ffmpeg -f image2 -i %d.png -vcodec libx264 -pix_fmt yuv420p -s 1200x1200 video.mp4
	mv video.mp4 ../$shape.mp4
done
