.PHONY: run
fast:
	uvicorn main:app --host 0.0.0.0 --port 8080 --reload

clean:
	rm static/images/*.jpg


update:
	docker compose down 
	docker compose pull
	docker compose up -d --build

restart: 
	docker compose restart

remove:
	docker compose down -v
	docker compose rm -f

curl_data:
	curl -X POST -H "Content-Type: application/json" -d @data.json 127.0.0.1:8080/items