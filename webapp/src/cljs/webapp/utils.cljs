(ns webapp.utils)

(defn parse-json
  ([s] (parse-json s true))
  ([s keywordize-keys?]
     (js->clj (js/JSON.parse s) :keywordize-keys keywordize-keys?)))

