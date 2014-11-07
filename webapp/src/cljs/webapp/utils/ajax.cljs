(ns webapp.utils.ajax
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [cljs-http.client :as http]
            [webapp.utils :as utils])
  (:refer-clojure :exclude [get]))

(def ^:dynamic *base-url* nil)

(defn delete
  [url]
  ;; TODO
  nil
  )

(defn post
  ([url] (post url {}))
  ([url data] (post url data true))
  ([url data relative?]
   (go (let [{:keys [status body]} (<! (http/post (if relative?
                                                    (str *base-url* url)
                                                    url)
                                                  {:json-params data
                                                   ;; TODO: kill?
                                                   :headers {"content-type" "application/json"
                                                             "accept" "application/json"}
                                                   }))]
           (when (= status 200)
             body)))))

(defn get
  ([url] (get url {}))
  ([url data] (get url data true))
  ([url data relative?]
     (go (let [{:keys [status body]} (<! (http/get (if relative?
                                                     (str *base-url* url)
                                                     url)
                                                   {:query-params data}))]
           (when (= status 200)
             body)))))

(defn get-json
  [& args]
  (go (utils/parse-json (<! (apply get args)))))

(defn post-json
  [& args]
  (go (utils/parse-json (<! (apply post args)))))
