<?

$time = time();
$ip = $_SERVER['REMOTE_ADDR'];
$action = $_REQUEST["action"];
$SERVER_TIMEOUT = 20;

if (!$action)
    die();

$db = sqlite_open('hosts.db', 0666, $error);
if (!$db) die ($error);

$query = "CREATE TABLE hosts(" . 
       "name text, time int)";
$ok = @sqlite_exec($db, $query, $error);

if (!$ok && $error != "table hosts already exists")
   die("Cannot execute query. $error");

//Delete expired entries
$query = "DELETE FROM hosts WHERE time < " . ($time-$SERVER_TIMEOUT);
$ok = sqlite_exec($db, $query, $error);
if (!$ok) die("Cannot delete expired times" . $error);

if ($action == "ping")
{
    $query = "INSERT INTO hosts VALUES(\"" . $ip . "\", " . $time . ")";
    $ok = sqlite_exec($db, $query, $error);
    if (!$ok) die("Cannot insert new time. " . $error);
}

if ($action == "gethosts")
{
    $query = "SELECT name, time FROM hosts ORDER BY time DESC LIMIT 10";
    $result = sqlite_query($db, $query);
    $hosts = array();
    if ($result)
    {
        while ($row = sqlite_fetch_array($result, SQLITE_ASSOC))
        {
            if (!in_array($row["name"], $hosts))
            {
                echo $row["name"] . " ";
                $hosts[] = $row["name"];
            }
        }
    }

}

sqlite_close($db);

?>