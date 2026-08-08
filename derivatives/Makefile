build:
	 g++ -std=c++17 -O2 -o derivative_trend derivative-trends.cpp

run: build
	./derivative_trend

clean:
	rm derivative_trend

saveImage:
	python3 -c "import cairosvg; cairosvg.svg2png(url='cover.svg', write_to='cover.png', output_width=1360, output_height=850)"
	python3 -c "import cairosvg; cairosvg.svg2png(url='cover.svg', write_to='cover.png', output_width=1360, output_height=850)"