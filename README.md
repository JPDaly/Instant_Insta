# Instant_Insta
Instant_Insta will automatically update your Instagram account based on a hashtag.

Instant_insta achieves this by downloading images off instagram based on a hashtag of your choice. It then attempts to remove unrelated images using a KMeans algorithm.
At the moment the only image that it's able to create is the average of all the images downloaded. 
Unless you use your imagination this approach doesn't produce images that represent the hashtag very well.

Note:
This program relies on the use of a webdriver. I've chosen to use Chromedriver (which can be downloaded at "http://chromedriver.chromium.org/") however, I believe there are others. Chromedriver can be found in Resources\chromedriver.exe.
I'm assuming that it's okay to use chromedriver in this way and to include it in my repository because it's open source.
