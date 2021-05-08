NSPACE="harrijin"
APP="pandemic-mobility"
VER="latest"
RPORT="6393"
FPORT="5013"
UID="869722"
GID="816966"

list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'


build-db:
	docker build -t ${NSPACE}/${APP}-db:${VER} \
                     -f docker/Dockerfile.db \
                     ./

build-api:
	docker build -t ${NSPACE}/${APP}-api:${VER} \
                     -f docker/Dockerfile.api \
                     ./
build-wrk:
	docker build -t ${NSPACE}/${APP}-wrk:${VER} \
                     -f docker/Dockerfile.wrk \
                     ./

push-db:
	docker push ${NSPACE}/${APP}-db:${VER} 

push-api:
	docker push ${NSPACE}/${APP}-api:${VER}
push-wrk:
	docker push ${NSPACE}/${APP}-wrk:${VER}
	
push-all: push-db push-api push-wrk

clean-db:
	docker ps -a | grep ${NSPACE}-db | awk '{print $$1}' | xargs docker rm -f

clean-api:
	docker ps -a | grep ${NSPACE}-api | awk '{print $$1}' | xargs docker rm -f

clean-wrk:
	docker ps -a | grep ${NSPACE}-wrk | awk '{print $$1}' | xargs docker rm -f



build-all: build-db build-api build-wrk

clean-all: clean-db clean-api clean-wrk




compose-up:
	# VER=${VER} docker-compose -f docker/docker-compose.yml pull
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} up -d --build ${NSPACE}-db
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} up -d --build ${NSPACE}-api
	sleep 5
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} up -d --build ${NSPACE}-wrk

compose-down:
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} down

k8-apply:
	kubectl apply -f kubernetes/db
	kubectl apply -f kubernetes/api
	kubectl apply -f kubernetes/worker

