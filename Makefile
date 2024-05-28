.PHONY: run
fast:
	uvicorn main:app --host 0.0.0.0 --port 5000 --reload

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
