## Essays / static content on [www.moderndescartes.com](http://www.moderndescartes.com)

This is a static site generator that compiles a set of markdown files, generates HTML, and then pushes HTML/CSS/JS to a Google Cloud Storage bucket for serving.

# Instructions to myself
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

Read docs at [https://cloud.google.com/storage/docs/hosting-static-website](https://cloud.google.com/storage/docs/hosting-static-website). In particular, you'll want to

- verify that you control the domain name
- make a bucket with the name of your website. (and update config with the website URL)
- set DNS to point at `c.storage.googleapis.com.` with a CNAME (trailing dot not a typo). (Note: CNAME does not support the root domain (domain.com), but only subdomain.domain.com. You'll want to set an alias to forward domain.com to subdomain.domain.com; implementation differs by DNS provider.)
- after all this is set up, execute the one-time bucket setup calls

```
gsutil web set -m index.html -e 404.html gs://$WEBSITE_URL
gsutil iam ch allUsers:objectViewer gs://$WEBSITE_URL
```

Finally, you'll want to [install pandoc](https://pandoc.org/installing.html)

# How to compile/deploy
```
python3 make.py
./push
```

If you change anything about the compilation step, do a manual check over essays exercising various features - in particular:
    - fractal plants (javascript embedded snippets)
    - probability manipulations (heavy TeX)
    - hyperloglog (code blocks)
    - bitpacking compression (tables)
    - convnet edge detection (images)

# BigQuery analytics
```
bq load --skip_leading_rows=1 --project_id=$PROJECT_ID --allow_quoted_newlines access_logs.usage gs://moderndescartes-accesslogs/www.moderndescartes.com_usage* cloud_storage_usage_schema_v0.json
```

```
WITH temp AS (SELECT
  EXTRACT(DATE FROM TIMESTAMP_MICROS(time_micros)) as date_,
  REGEXP_EXTRACT(cs_uri, r'essays/([^/?]*)') as essay_shortname
from `access_logs.usage`
)
SELECT * from temp
WHERE essay_shortname is not null and essay_shortname not like 'rss.xml%'
```