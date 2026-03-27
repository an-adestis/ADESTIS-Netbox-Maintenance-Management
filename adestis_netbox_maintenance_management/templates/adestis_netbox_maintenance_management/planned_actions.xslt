<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes"/>

  <xsl:template match="/planned-actions">
    <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          h1 { text-align: center; }
          table { width: 100%; border-collapse: collapse; margin-top: 20px; }
          th, td { border: 1px solid #ccc; padding: 5px; text-align: left; }
          th { background-color: #eee; }
          .logo { width: 100px; display: block; margin: 0 auto 10px auto; }
        </style>
      </head>
      <body>
        <!-- Logo -->
        <img src="/static/adestis_netbox_maintenance_management/planned_actions/logo.png" class="logo" alt="Logo"/>
        <h1>Planned Actions</h1>
        <table>
          <tr>
            <th>Date</th>
            <th>Action</th>
            <th>Comments</th>
            <th>Maintenance Actions</th>
            <th>VMs</th>
            <th>Devices</th>
          </tr>
          <xsl:for-each select="group">
            <xsl:for-each select="action">
              <tr>
                <td><xsl:value-of select="../@date"/></td>
                <td><xsl:value-of select="name"/></td>
                <td><xsl:value-of select="comments"/></td>
                <td>
                  <xsl:for-each select="maintenance-actions/maintenance-action">
                    <div><xsl:value-of select="."/></div>
                  </xsl:for-each>
                </td>
                <td>
                  <xsl:for-each select="vms/vm">
                    <div><xsl:value-of select="name"/> (<xsl:value-of select="comment"/>)</div>
                  </xsl:for-each>
                </td>
                <td>
                  <xsl:for-each select="devices/device">
                    <div><xsl:value-of select="name"/> (<xsl:value-of select="comment"/>)</div>
                  </xsl:for-each>
                </td>
              </tr>
            </xsl:for-each>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>