# image-scraper

> Little script which downloads all recent images from a given subreddit.

Currently the subreddit is hardcoded to [/r/MostBeautiful](https://www.reddit.com/r/MostBeautiful/). Feel free to change the subreddit in the `image-scraper.py`-file.

## Run in docker container

```bash
docker build -t image-scraper /.../image-scraper
mkdir -p /.../image-scraper/imgs
docker run --rm --name image-scraper -v /.../image-scraper/imgs:/app/imgs image-scraper
```

We're mounting a directory `/.../image-scraper/imgs` into the container. The `image-scraper` script writes all downloaded files there. (It also checks what files are already downloaded and skips them.)

## First run

You need a Reddit account for the `image-scraper` to work.

1. Assuming an account head over to https://www.reddit.com/prefs/apps/
2. Click on **are you a developer? create an app...**
3. Choose a name
4. Select **script** for personal use
5. Enter a description
6. Paste `http://localhost:8080` into the redirect uri
7. Click on **create app**

Now paste the client id (14 characters) and the secret (27 characters) into the `image-scraper.py`. Add your username and password (from which the app has been created).

You should run the `image-scraper` with the `--all` flag at the first run. Without that flag the script will check only the first 100 posts in the subreddit. With `--all` the first 1000 posts are evaluated. (More is not possible due to the `limit` constraints of the Reddit API.) For example:

```bash
mkdir -p /.../image-scraper/imgs
docker run --rm --name image-scraper -v /.../image-scraper/imgs:/app/imgs image-scraper --all
```

(In [/r/MostBeautiful](https://www.reddit.com/r/MostBeautiful/) you will get ca. the images of the last two months when using `--all`. Without `--all` you'll get only the last few weeks.)

## Automated downloads

Since ca. 10 images are posted every day on [/r/MostBeautiful](https://www.reddit.com/r/MostBeautiful/) we will download new images every day. For that we will create SystemD unit files (a service-file and a timer-file).

`systemctl cat image-scraper.service`:

```systemd
# /etc/systemd/system/image-scraper.service
[Unit]
Description=Reddit image scraper
After=network-online.target docker.service

[Service]
Type=oneshot
ExecStart=/usr/bin/docker run --rm --name image-scraper -v /.../image-scraper/imgs:/app/imgs image-scraper
```

`systemctl cat image-scraper.timer`:

```systemd
# /etc/systemd/system/image-scraper.timer
[Timer]
OnCalendar=daily
Unit=image-scraper.service

[Install]
WantedBy=multi-user.target
```

## How are posts filtered, decisions what to download

The `image-scraper` filters posts so that only "good" images are downloaded. Here are the filtering rules:

* Do not download if already downloaded.
* Do not download if score is below `+100`.
* Do not download if reddit does not provide a preview in the post (so no direct image linked).
* Do not download if the resolution is below `1920x1080`.
