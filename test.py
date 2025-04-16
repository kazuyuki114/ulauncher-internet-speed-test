import speedtest as st

# Create Speedtest instance with a custom timeout (without threads)
speed_tester = st.Speedtest(timeout=5)

# Get the best server information as a dictionary
best_server = speed_tester.get_best_server()

# Retrieve download, upload, and ping information using the threads parameter in method calls
download_speed = speed_tester.download(threads=2) / (1024 * 1024)  # Convert from bits to Mbps
upload_speed = speed_tester.upload(threads=2) / (1024 * 1024)        # Convert from bits to Mbps
ping = speed_tester.results.ping

# Extract server details
host_name = best_server.get('host')
server_city = best_server.get('name')       # e.g. the city
server_country = best_server.get('country')  # e.g. the country
server_sponsor = best_server.get('sponsor')    # often the company or network that operates the server

print(f"Selected Server: {server_sponsor} (Host: {host_name}) located in {server_city}, {server_country}")
print(f"Download speed: {download_speed:.2f} Mbps")
print(f"Upload speed: {upload_speed:.2f} Mbps")
print(f"Ping: {ping} ms")
