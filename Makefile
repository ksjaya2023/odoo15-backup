
## WEB_DB_NAME=Prager_Testing
WEB_DB_NAME=pg_migration
DOCKER=docker
DOCKER_COMPOSE=${DOCKER} compose
CONTAINER_ODOO=odoo
CONTAINER_ODOO_CONSOLE=odoo15
CONTAINER_ODOO_PGUSER=odoopg
CONTAINER_ODOO_PGPWD=odoopg
CONTAINER_DB=odoo-postgres

help:
	@echo "Available Target"
	@echo "  start              Start The Compose with daemon"
	@echo "  stop               Stop The Compose"
	@echo "  restart            Restart The Compose"
	@echo "  console            Odoo Interactive Console"
	@echo "  psql               PostgreSQl interactive shell"
	@echo "  logs a=odoo        Log The Odoo Container"
	@echo "  logs a=db          Log PostgreSQL Container"
	@echo "  htop               Monitor CPU & Process"
	@echo "  free-m             Monitor Memory"
	@echo "  df-h               Monitor Disk"
	@echo "  nload              Monitor Jaringan"
	@echo "  tmux-n             Create New Session odoo"
	@echo "  tmux-c             Close Session odoo"
	@echo "  tmux-j             Joint Session odoo"

start:
	sudo $(DOCKER_COMPOSE) up -d
stop:
	sudo $(DOCKER_COMPOSE) down
restart:
	sudo $(DOCKER_COMPOSE) restart
console:
	sudo $(DOCKER) exec -it $(CONTAINER_ODOO_CONSOLE) odoo shell --db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(CONTAINER_ODOO) -w $(CONTAINER_ODOO)
psql:
	sudo $(DOCKER) exec -it $(CONTAINER_DB) psql -U $(CONTAINER_ODOO_PGUSER) -d $(WEB_DB_NAME) \


logs:
	@if [ "$(a)" = "odoo" ]; then \
		sudo $(DOCKER_COMPOSE) logs -f $(CONTAINER_ODOO); \
	elif [ "$(a)" = "db" ]; then \
		sudo $(DOCKER_COMPOSE) logs -f $(CONTAINER_DB);\
	else \
		echo "Invalid logs target. Use 'make logs odoo' or 'make logs db'  "; \
	fitm
htop:
	sudo htop
free-m: 
	sudo free -m
df-h:
	sudo df -h
nload: 
	sudo nload
tmux-n:
	tmux new -s odoo
tmux-c:
	tmux kill-session -t odoo
tmux-j:
	tmux attach -t odoo

# logs:
#	(call log_target,$(word 2,$(MAKECMDGOALS)))

.PHONY: start stop restart console psql logs odoo db, htop, free-m, df-h, nload, tmux-n, tmux-c, tmux-j 

