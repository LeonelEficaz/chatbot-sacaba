$uri = "http://127.0.0.1:5000/chat"
$body = [System.Text.Encoding]::UTF8.GetBytes('{"message":"rumi_llaqta","language":"auto"}')
$c = [System.Net.WebRequest]::Create($uri)
$c.Method = "POST"
$c.ContentType = "application/json"
$c.GetRequestStream().Write($body, 0, $body.Length)
$r = $c.GetResponse()
$stream = $r.GetResponseStream()
$reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
$result = $reader.ReadToEnd()
Write-Host "Response: $result"
$reader.Close()
$stream.Close()
$r.Close()