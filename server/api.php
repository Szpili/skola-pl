<?php
header('Content-Type: application/json; charset=utf-8');
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$allow = [
  'https://skola.weryta.com',
  'https://szpili.github.io',
  'http://127.0.0.1',
  'http://localhost',
];
foreach ($allow as $o) {
  if ($origin === $o || strpos($origin, $o) === 0) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Vary: Origin');
    break;
  }
}
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') { http_response_code(204); exit; }

function fail($code, $msg) {
  http_response_code($code);
  echo json_encode(['ok' => false, 'error' => $msg]);
  exit;
}

$cfgFile = __DIR__ . '/config.php';
if (!is_file($cfgFile)) fail(500, 'config.php missing');
$cfg = require $cfgFile;

try {
  $db = new PDO(
    'mysql:host=' . $cfg['host'] . ';dbname=' . $cfg['name'] . ';charset=utf8mb4',
    $cfg['user'],
    $cfg['pass'],
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
  );
} catch (PDOException $e) {
  fail(500, 'db');
}

$db->exec(
  'CREATE TABLE IF NOT EXISTS votes (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    pool VARCHAR(80) NOT NULL,
    gx TINYINT UNSIGNED NOT NULL,
    gy TINYINT UNSIGNED NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY pool_created (pool, created_at)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'
);

$action = $_GET['action'] ?? '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'GET' && $action === 'ping') {
  echo json_encode(['ok' => true]);
  exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'GET' && $action === 'tally') {
  $pool = $_GET['p'] ?? '';
  if (!preg_match('/^[a-z0-9-]{3,80}$/', $pool)) fail(400, 'pool');
  $st = $db->prepare('SELECT gx, gy, COUNT(*) AS n FROM votes WHERE pool = ? GROUP BY gx, gy');
  $st->execute([$pool]);
  $cells = array_fill(0, 5, array_fill(0, 5, 0));
  $total = 0;
  foreach ($st as $row) {
    $gx = (int)$row['gx']; $gy = (int)$row['gy']; $n = (int)$row['n'];
    if ($gx <= 4 && $gy <= 4) { $cells[$gy][$gx] = $n; $total += $n; }
  }
  echo json_encode(['ok' => true, 'pool' => $pool, 'total' => $total, 'cells' => $cells]);
  exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
  $raw = json_decode(file_get_contents('php://input'), true) ?: [];
  $pool = $raw['p'] ?? ($_POST['p'] ?? '');
  $gx = isset($raw['gx']) ? (int)$raw['gx'] : (int)($_POST['gx'] ?? -1);
  $gy = isset($raw['gy']) ? (int)$raw['gy'] : (int)($_POST['gy'] ?? -1);
  if (!preg_match('/^[a-z0-9-]{3,80}$/', $pool)) fail(400, 'pool');
  if ($gx < 0 || $gx > 4 || $gy < 0 || $gy > 4) fail(400, 'cell');
  $st = $db->prepare('INSERT INTO votes (pool, gx, gy) VALUES (?, ?, ?)');
  $st->execute([$pool, $gx, $gy]);
  echo json_encode(['ok' => true, 'id' => (int)$db->lastInsertId()]);
  exit;
}

fail(400, 'action');
