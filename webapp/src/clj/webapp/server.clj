(ns webapp.server
  (:require [org.httpkit.server :as httpkit]
            [com.stuartsierra.component :as component]
            ring.middleware.params
            ring.middleware.keyword-params
            ring.middleware.json
            [webapp.routes :as routes]
            [webapp.utils.logging :as log]))

;; TODO: kill - its for figwheel
(defn wrap-allow-credentials
  "middleware function to allow crosss origin"
  [handler]
  (fn [request]
   (let [response (handler request)]
     (assoc-in response [:headers "Access-Control-Allow-Credentials"]
               "true"))))

;; TODO: kill - its for figwheel
(defn wrap-allow-cross-origin
  "middleware function to allow crosss origin"
  [handler]
  (fn [request]
    (let [response (handler request)]
      (assoc-in response [:headers "Access-Control-Allow-Origin"]
                "http://localhost:3449"))))

(defn wrap-request-logging
  "Middleware wrapper to log all incoming requests."
  [handler]
  (fn [{:keys [request-method uri session params] :as req}]
    (let [resp (handler req)]
      (log/info (format "REQUEST%s %s, session=%s, params=%s"
                        request-method uri session params))
      resp)))

(defn start-server
  [{:keys [port]}]
  (httpkit/run-server
    (-> routes/app
        ring.middleware.keyword-params/wrap-keyword-params
        ring.middleware.json/wrap-json-params
        ring.middleware.params/wrap-params
        ;; TODO: kill
        #_wrap-allow-cross-origin
        #_wrap-allow-credentials
        wrap-request-logging)
    {:port port
     :thread 8
     :worker-name-prefix "server-"}))

(defrecord ServerComponent [server ;; callback to cancel started server
                            database ;; mongo database
                            port ;; port num
                            ]
  component/Lifecycle
  (start [this]
    ;; In the 'start' method, a component may assume that its
    ;; dependencies are available and have already been started.
    (log/info "Starting server on port" port)
    (if server
      this
      (let [new-server (start-server {:port port})]
        (assoc this :server new-server))))
  (stop [this]
    ;; Likewise, in the 'stop' method, a component may assume that its
    ;; dependencies will not be stopped until AFTER it is stopped.
    ((:server this) :timeout 1000)
    (log/info "Stopping server")
    (dissoc this :server)))

(defn server-component
  [port]
  (map->ServerComponent {:port port}))
