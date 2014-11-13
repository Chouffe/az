(ns webapp.utils.logging
  (:require [clojure.tools.logging :as log]))

(def trace println)
(def debug println)
(def info println)
(def warn println)
(def error println)

