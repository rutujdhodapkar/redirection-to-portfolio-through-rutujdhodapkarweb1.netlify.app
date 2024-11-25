const ftp = require('basic-ftp');  // Use an FTP client library

exports.handler = async (event) => {
  const client = new ftp.Client();
  client.ftp.verbose = true;

  const ftpServer = 'ftp://your-ftp-server'; // Replace with your FTP server address
  const user = 'your-ftp-username';          // Replace with your FTP username
  const password = 'your-ftp-password';      // Replace with your FTP password
  const filePath = '/path/to/messages.txt';  // Shared file on FTP server

  try {
    await client.access({
      host: ftpServer,
      user: user,
      password: password,
      secure: true  // Use SFTP for security
    });

    if (event.httpMethod === 'POST') {
      // Send a message (append to file)
      const { message } = JSON.parse(event.body);
      await client.append(Buffer.from(message, 'utf-8'), filePath);
      return {
        statusCode: 200,
        body: JSON.stringify({ message: "Message sent!" })
      };
    } else {
      // Get messages from the file
      const content = await client.downloadToBuffer(filePath);
      const messages = content.toString('utf-8');
      return {
        statusCode: 200,
        body: JSON.stringify({ messages })
      };
    }
  } catch (error) {
    console.error("FTP Error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Error with FTP operation" })
    };
  } finally {
    client.close();
  }
};
