<?php
/* Helper for POI vulnerabilities*/

function find_POI_targets($target) {
        $magic_methods = Array("__destruct", "__wakeup");
        $class_list = get_declared_classes();
        foreach($class_list as $class) {
                $method_list = get_class_methods($class);
                if (count(array_intersect($method_list, $magic_methods)) > 0) {
                        $reflection = new ReflectionClass($class);
                        if ($reflection->isUserDefined()) {
                                echo "[+] Interesting class:" . $class . "\n";
                        }
                }
        }
}

?>
