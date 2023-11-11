# ДЗ_8 Monitoring & Allerting
## _Настройка мониторинга и аллертинга метрик модели_
## _Использование инструментов: Prommetheus, Grafana_

1. Процесс мониторинга модели начинается с написания модели в виде сервиса, предоставляющего клиенту предикт - app9.py
   У сервиса есть метод predict, возвращающий предсказание факта фрода по входной строке, генерируемой исходя из введенного в запросе числа
   У сервиса так же имеется ручка metrics, собирающая значение количества предиктов класса ноль
2. Для выполнения задания создана виртуальная машина, на ней установлены все необхдимые ресурсы:
   - yc (https://cloud.yandex.ru/docs/cli/quickstart);
   - Docker (https://docs.docker.com/get-docker/);
   - Kubectl (https://kubernetes.io/docs/tasks/tools/install-kubectl/);
   - envsubst;
   - git;
   - ssh;
   - curl.
     
     Вход на ВМ осуществляется по ssh
3. Настроена консольная утилита для работы с облаком
   id каталога:
   ``` sh
   echo "export FOLDER_ID=folder-id-here" >> ~/.bashrc && . ~/.bashrc
   echo $FOLDER_ID
   yc config set folder-id $FOLDER_ID
   ```
    список виртуальных машин в каталоге:
     ``` sh
    yc compute instance list
     ```
4. В Yandex Cloud развернут кластер Managed K8S с группой из 3х узлов. Кластер сконфигурирован:
    ``` sh
    yc managed-kubernetes cluster list
    echo "export K8S_ID=k8s-id-here" >> ~/.bashrc && . ~/.bashrc
    echo $K8S_ID
    yc managed-kubernetes cluster --id=$K8S_ID get
    yc managed-kubernetes cluster --id=$K8S_ID list-node-groups
    ```
    
    В конфигурационный файл добавлены учетные данные:
    ``` sh
    yc managed-kubernetes cluster get-credentials --id=$K8S_ID --external
    cat ~/.kube/config
    ```
5. Создано Container Registry и сохранен id реестра
     ``` sh
    echo "export REGISTRY_ID=registry-id-here" >> ~/.bashrc && . ~/.bashrc
    yc container registry list
    yc container registry get $REGISTRY_ID
    ```
6. Настроена аутентификация в Docker
    ``` sh
    yc container registry configure-docker
    cat ~/.docker/config.json
    ```
7. Собран и загружен Docker-образ в Container Registry
    Перейдя в директорию /monitor
     ``` sh
    sudo docker build . --tag cr.yandex/$REGISTRY_ID/lab-demo:v1
    sudo docker images
    docker push cr.yandex/$REGISTRY_ID/lab-demo:v1
    yc container image list
    ```
8. Установлено prometheus-community
     ``` sh
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update    
    helm install monitoring prometheus-community/kube-prometheus-stack
    ```
10. Развернуты сервисы для деплоя, prometheus и grafana
    ``` sh
    kubectl apply -f k8s/deployment.yml
    kubectl apply -f k8s/service.yml
    kubectl apply -f k8s/monitoring.yml
    kubectl apply -f k8s/prom_rbac.yml
    ```
11. Для работы в браузере локального компьютера необходимо прокинуть порты не только изх контейнера, но и с ВМ на локалхост
    Для графаны и прометеуса
    ``` sh
    kubectl port-forward svc/prometheus-operated 9090:9090 -n default --address 0.0.0.0
    kubectl port-forward svc/monitoring-grafana 8082:80 -n default  --address 0.0.0.0
    ```
    Для сервиса
    ``` sh
    kubectl get pods
    kubectl port-forward <titanic pods name> 8000:8000 -n default  --address 0.0.0.0
    ```
12. Скриншоты успешности вышеописанных этапов    
Запуск контейнера
<image src="/screens/1. container running.jpg" alt="1">
Контейнер функционирует в клауде
<image src="screens/2. container in yc.jpg" alt="2">
Развернуты сервисы
<image src="screens/3. all ymls applied.jpg" alt="3">
Запуск прометеуса
<image src="screens/4. prometeus run.jpg" alt="4">
Запуск графана (admin/prom-operator)
<image src="screens/5. grafana run.jpg" alt="5">
Запуск сервиса
<image src="screens/6. service run.jpg" alt="6">
<image src="screens/7. service run2.jpg" alt="7">
Ручка metrics
<image src="screens/8. metrics.jpg" alt="8">
История обращений к сервису
<image src="screens/9. requests history.jpg" alt="9">
14. В графана построен дашборд метрики количества предиктов нулевого класса и аллерт, срабатывающий в случае, когда количество таковых превышает 10  

15. Скриншоты успешности построения дэшборда и аллертов

Отображение метрики в прометеусе
<image src="screens/10. predict total in prometheus.jpg" alt="10">
Первый сбор метрики в графане
<image src="screens/11. predict total grafana 1.jpg" alt="11">
Несколько нулевых предиктов подряд
<image src="screens/12. predict total grafana 2.jpg" alt="12">
Изменения на дэшборде при проведении запросов
<image src="screens/13. dash1.jpg" alt="13">
<image src="screens/14. dash2.jpg" alt="14">
<image src="screens/15. dash3.jpg" alt="15">
Правило на allert
<image src="screens/16. allert rule.jpg" alt="16">
Allert pending (дэшборд сопровождается сердечком)
<image src="screens/17. allert pending.jpg" alt="17">
Срабатывание аллерта при наступлении события count=10 (сопровождается разбитым сердечком)
<image src="screens/18. allert allerting.jpg" alt="18">

16. По завершении работы над заданием ресурсы клауда удалены


