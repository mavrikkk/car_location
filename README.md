# car_location

<h1>Description</h1>
<h3>RUS</h3>
<p>Данная интеграция позволяет подключить любой GPS трекер (совместимый с <a href='https://livegpstracks.com/'>livegpstracks</a>) к вашему HomeAssistant.</p>
<h3>ENG</h3>
<p>This integration allows you to connect any GPS Tracker ( compatible with <a href='https://livegpstracks.com/'>livegpstracks</a> service) to HomeAssistant.</p>

<h1>Installation</h1>
<h3>RUS</h3>
<p>Регистрируемся в сервисе livegpstracks и подключаем свой трекер (на сайте есть подробные инструкции для различных моделей). После этого через панель инструментов на сайте создаем приватную ссылку для слежения. Ссылка имеет вид:</p> 
<pre><code>
https://livegpstracks.com/dv_USERID.html
</code></pre>
<p>где USERID – цифровой ID вашей шары, он пригодится нам вдальнейшем</p>
<p>Содержимое папки "car_location" скопировать в директорию "config_folder_homeassistant/custom_components/car_location". Не забывайте про права на созданные директории и файлы.</p>
<h3>ENG</h3>
<p>You need to register in the livegpstracks service and connect the tracker (the site has detailed instructions for various models) to it. After that, through the toolbar on the site we create a private link for tracking. The link looks like:</p> 
<pre><code>
https://livegpstracks.com/dv_USERID.html
</code></pre>
<p>here USERID – is ID of your livegpstracks share, it will be needed to us further </p>
<p>Place the "car_location" folder to "config_folder_homeassistant/custom_components/". Do not forget about the rights to created folders and files.</p>

<h1>Configuration</h1>
<h3>RUS</h3>
<p>Добавьте в ваш файл конфигурации "configuration.yaml" следующие строки:</p>
<pre><code>
sensor:
  - platform: car_location
    name: car_sensor
    user: your_username
    myid: 'your_share_id'
</code></pre>
<p>здесь "your_username" – пользователь, под которым вы регистрировались в сервисе livegpstracks, "your_share_id" – цифровой ID, который присваивается расшаренной ссылке</p>
<h3>ENG</h3>
<p>Add the following lines in the "configuration.yaml" file:</p>
<pre><code>
sensor:
  - platform: car_location
    name: car_sensor
    user: your_username
    myid: 'your_share_id'
</code></pre>
<p>here "your_username" is the username, you registered with on livegpstracks, "your_share_id" is ID of your livegpstracks share.</p>

<h1>TODO</h1>
<h3>RUS</h3>
<p>- ???</p>
<p>- исправить корявый английский</p>
<h3>ENG</h3>
<p>- ???</p>
<p>- edit BAD English</p>
