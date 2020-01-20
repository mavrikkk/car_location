**Description (Описание)**
<p>This integration allows you to connect any GPS Tracker ( compatible with <a href='https://livegpstracks.com/'>livegpstracks</a> service) to HomeAssistant (Данная интеграция позволяет подключить любой GPS трекер (совместимый с <a href='https://livegpstracks.com/'>livegpstracks</a>) к вашему HomeAssistant)</p>



**Installation (Установка):**
<p>You need to register in the livegpstracks service and connect the tracker (the site has detailed instructions for various models) to it. After that, through the toolbar on the site we create a private link for tracking. The link looks like:</p> 
<pre><code>
https://livegpstracks.com/dv_USERID.html
</code></pre>
<p>here USERID – is ID of your livegpstracks share, it will be needed to us further </p>
<p>Then install this integration</p>

<p>Регистрируемся в сервисе livegpstracks и подключаем свой трекер (на сайте есть подробные инструкции для различных моделей). После этого через панель инструментов на сайте создаем приватную ссылку для слежения. Ссылка имеет вид:</p> 
<pre><code>
https://livegpstracks.com/dv_USERID.html
</code></pre>
<p>где USERID – цифровой ID вашей шары, он пригодится нам вдальнейшем</p>
<p>После этого установите данную интеграцию</p>



**Example configuration.yaml:**

```yaml
sensor:
  platform: car_location
  name: car_location
  user: your_username
  myid: 'your_share_id'
```



**Configuration variables:**  
  
key | description  
:--- | :---  
**platform (Required)** | The platform name (имя платформы)
**name (Option)** | The name of this element in HA interface (имя элемента в интерфейсе HA)
**haddr (Required)** | base_url of HA (base_url вашего HA)
**entityid (Required)** | the HA entityid of your device_tracker (это ID вашего устройства, за которым будете наблюдать)
**timezone (Required)** | is your timezone, for example '+03:00' (ваш часовой пояс, например '+03:00')
**token (Required)** | the access token previously received in the frontend of HomeAssistant to use REST API (предварительно полученный во фронтенде HomeAssistant токен доступа для использования REST API)
  
  
  
**!!!IMPORTANT!!! after installation instructions**

<p>After installation the map will be at your_address_homeassistant/local/route/index.html. If you wish, you can add it to the HA menu using panel_iframe or to any HA window via the lovelace card “iframe” (После установки карта будет доступна по прямой ссылке: your_address_homeassistant/local/route/index.html. При желании вы можете добавить ее в меню HA с помощью panel_iframe или в любое окно HA через lovelace card “iframe”).</p>



**Screenshots (very blurred!!!)**

![example][exampleimg]



***

[exampleimg]: map.jpeg
