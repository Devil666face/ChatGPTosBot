[Unit]
Description=Chat GPT Open source bot
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=%PWD%
ExecStart=%PWD%/main.bin 
Restart=on-failure

[Install]
WantedBy=multi-user.target
