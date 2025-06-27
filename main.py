import json, time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from extractor import OddsExtractor

DRIVER_PATH   = r"C:\Users\Brand\AppData\Local\edgedriver_win64\msedgedriver.exe"
TARGET_URL    = "https://www.365scores.com/football/live"
RAW_LOG       = "raw_365scores.jsonl"
PROCESSED_LOG = "odds_365scores.jsonl"

# Nuevo keyword para capturar los JSON de allscores con showOdds=true
KEYWORDS = [
  "webws.365scores.com/web/games/allscores",
  "showOdds=true"
]


JS_INTERCEPT = """
window._requests = [];
(function(open, send) {
  XMLHttpRequest.prototype.open = function(m, u) {
    this._url = u; return open.apply(this, arguments);
  };
  XMLHttpRequest.prototype.send = function() {
    this.addEventListener('load',()=>{
      window._requests.push({
        url: this._url,
        status: this.status,
        body: this.responseText
      });
    });
    return send.apply(this, arguments);
  };
})(XMLHttpRequest.prototype.open, XMLHttpRequest.prototype.send);

(function(fetch){
  window.fetch = function(){
    return fetch.apply(this,arguments).then(resp=>{
      resp.clone().text().then(txt=>{
        window._requests.push({
          url: resp.url,
          status: resp.status,
          body: txt
        });
      });
      return resp;
    });
  };
})(window.fetch);
"""

def main():
    service = Service(executable_path=DRIVER_PATH, log_path='NUL')
    opts = Options()
    opts.use_chromium = True
    opts.add_argument("--headless")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    opts.add_argument("--log-level=3")

    driver = webdriver.Edge(service=service, options=opts)

    # Inyectamos el interceptor ANTES de get()
    driver.execute_cdp_cmd(
      "Page.addScriptToEvaluateOnNewDocument",
      {"source": JS_INTERCEPT}
    )

    driver.get(TARGET_URL)
    time.sleep(12)  # un poco más para asegurar que cargue ALLSCORES

    all_reqs = driver.execute_script("return window._requests")
    driver.quit()

    # DEBUG: mira cuántas requests capturó
    print(f"Total requests capturadas: {len(all_reqs)}")

    extractor = OddsExtractor()
    count = 0
    with open(RAW_LOG, 'w', encoding='utf-8') as raw_f, \
         open(PROCESSED_LOG, 'w', encoding='utf-8') as proc_f:

        for r in all_reqs:
            url = r.get("url", "")
            # acepto cualquiera de los dos fragmentos
            if not any(k in url for k in KEYWORDS):
                continue

            # Guardamos el raw JSON
            raw_f.write(json.dumps(r, ensure_ascii=False) + "\n")

            # Extraemos las odds
            for odd in extractor.extract(url, r.get('body','').encode()):
                proc_f.write(json.dumps(odd.__dict__, default=str) + "\n")
            count += 1

    print(f"[+] Escritas {count} entradas en {RAW_LOG} y {PROCESSED_LOG}")

if __name__ == "__main__":
    main()