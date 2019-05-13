# car_location

<h1>Description</h1>
<h3>RUS</h3>
<p>Данная интеграция позволяет подключить GPS трекер Sinotrack ST-901 к вашему HomeAssistant через посредника <a href='https://livegpstracks.com/'>livegpstracks</a></p>
<h3>ENG</h3>
<p>This integration allows you to connect Sinotrack ST-901 GPS Tracker to HomeAssistant through <a href='https://livegpstracks.com/'>livegpstracks</a> service</p>

<h1>How it works</h1>
<h3>RUS</h3>
<p></p>
<h3>ENG</h3>
<p></p>

<h1>Installation</h1>
<h3>RUS</h3>
<p></p>
<h3>ENG</h3>
<p></p>

<h1>Configuration</h1>
<h3>RUS</h3>
<p></p>
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
<p>here "your_username" is the username, you reg on livegpstracks, "your_share_id" is ID of your livegpstracks share.</p>

<h1>TODO</h1>
<h3>RUS</h3>
<p>- ???</p>
<h3>ENG</h3>
<p>- ???</p>
