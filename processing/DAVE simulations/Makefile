generate-data:
	@echo "Generating data from DAVE simulations"
	uv run process.py
	tippecanoe --force -zg --read-parallel \
		--coalesce-densest-as-needed \
		--extend-zooms-if-still-dropping \
		--accumulate-attribute=hour_0:mean \
		--accumulate-attribute=hour_1:mean \
		--accumulate-attribute=hour_2:mean \
		--accumulate-attribute=hour_3:mean \
		--accumulate-attribute=hour_4:mean \
		--accumulate-attribute=hour_5:mean \
		--accumulate-attribute=hour_6:mean \
		--accumulate-attribute=hour_7:mean \
		--accumulate-attribute=hour_8:mean \
		--accumulate-attribute=hour_9:mean \
		--accumulate-attribute=hour_10:mean \
		--accumulate-attribute=hour_11:mean \
		--accumulate-attribute=hour_12:mean \
		--accumulate-attribute=hour_13:mean \
		--accumulate-attribute=hour_14:mean \
		--accumulate-attribute=hour_15:mean \
		--accumulate-attribute=hour_16:mean \
		--accumulate-attribute=hour_17:mean \
		--accumulate-attribute=hour_18:mean \
		--accumulate-attribute=hour_19:mean \
		--accumulate-attribute=hour_20:mean \
		--accumulate-attribute=hour_21:mean \
		--accumulate-attribute=hour_22:mean \
		--accumulate-attribute=hour_23:mean \
		-o hourly_adult_population.pmtiles hourly_adult_population_wgs84.geojson
	cp hourly_adult_population.pmtiles ../../frontend/public/geodata/
	@echo "Data generated successfully"

upload:
	@echo "Uploading to CDN"
	
	s3cmd put --acl-public --guess-mime-type hourly_adult_population.pmtiles \
		"s3://$${BUCKET_NAME}/urbes-viz/hourly_adult_population.pmtiles"
	@echo "Upload complete"
	@echo "File available at: https://enacit4r-cdn.epfl.ch/urbes-viz/hourly_adult_population.pmtiles"

clean:
	@echo "Cleaning generated files"
	rm -f hourly_adult_population_wgs84.geojson
	rm -f hourly_adult_population.pmtiles
	@echo "Clean complete"

.PHONY: generate-data upload clean
