<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:output method="xml" indent="yes"/>

<xsl:template match="/">

<fo:root>

  <fo:layout-master-set>
    <fo:simple-page-master master-name="A4"
                           page-width="21cm"
                           page-height="29.7cm"
                           margin="2cm">
      <fo:region-body margin-top="3cm" margin-bottom="2cm"/>
      <fo:region-before extent="2cm"/>
      <fo:region-after extent="1cm"/>
    </fo:simple-page-master>
  </fo:layout-master-set>

  <fo:page-sequence master-reference="A4">
    <!-- Header -->
    <fo:static-content flow-name="xsl-region-before">
      <fo:block text-align="right">
        <fo:external-graphic src="url('adestis_netbox_maintenance_management/templates/planned_actions/logo.png')" content-width="3cm"/>
      </fo:block>
      <fo:block font-size="16pt" font-weight="bold" space-before="5pt">
        Planned Actions
      </fo:block>
    </fo:static-content>

    <!-- Footer -->
    <fo:static-content flow-name="xsl-region-after">
      <fo:block text-align="left">
        Generated on <xsl:value-of select="planned-actions/@created"/>
      </fo:block>
      <fo:block text-align="right">
        Page <fo:page-number/> / <fo:page-number-citation ref-id="end-of-doc"/>
      </fo:block>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">

      <xsl:for-each select="planned-actions/group">

        <fo:block font-size="12pt" space-before="10pt" font-weight="bold">
          Date: <xsl:value-of select="@date"/>
        </fo:block>

        <fo:table border="0.2mm solid #0a6c86" table-layout="fixed" width="100%">
          <fo:table-column column-width="5cm"/>
          <fo:table-column column-width="5cm"/>
          <fo:table-column column-width="6cm"/>

          <!-- Header, wiederholt auf jeder Seite -->
          <fo:table-header>
            <fo:table-row background-color="#0a6c86" color="white">
              <fo:table-cell><fo:block>Startzeit</fo:block></fo:table-cell>
              <fo:table-cell><fo:block>Endzeit</fo:block></fo:table-cell>
              <fo:table-cell><fo:block>Maintenance Action</fo:block></fo:table-cell>
            </fo:table-row>
          </fo:table-header>

          <fo:table-body>
            <xsl:for-each select="action">
              <fo:table-row>
                <fo:table-cell><fo:block><xsl:value-of select="start-time"/></fo:block></fo:table-cell>
                <fo:table-cell><fo:block><xsl:value-of select="end-time"/></fo:block></fo:table-cell>
                <fo:table-cell><fo:block><xsl:value-of select="name"/></fo:block></fo:table-cell>
              </fo:table-row>

              <fo:table-row>
                <fo:table-cell number-columns-spanned="3">
                  <fo:block font-style="italic" space-before="2pt" space-after="2pt">
                    <xsl:value-of select="comments"/>
                  </fo:block>

                  <fo:block font-weight="bold">VM</fo:block>
                  <fo:table>
                    <fo:table-body>
                      <xsl:for-each select="vms/vm">
                        <fo:table-row>
                          <fo:table-cell><fo:block><xsl:value-of select="name"/></fo:block></fo:table-cell>
                          <fo:table-cell><fo:block><xsl:value-of select="comment"/></fo:block></fo:table-cell>
                        </fo:table-row>
                      </xsl:for-each>
                    </fo:table-body>
                  </fo:table>

                  <fo:block font-weight="bold">Devices</fo:block>
                  <fo:table>
                    <fo:table-body>
                      <xsl:for-each select="devices/device">
                        <fo:table-row>
                          <fo:table-cell><fo:block><xsl:value-of select="name"/></fo:block></fo:table-cell>
                          <fo:table-cell><fo:block><xsl:value-of select="comment"/></fo:block></fo:table-cell>
                        </fo:table-row>
                      </xsl:for-each>
                    </fo:table-body>
                  </fo:table>

                </fo:table-cell>
              </fo:table-row>

            </xsl:for-each>
          </fo:table-body>

        </fo:table>

      </xsl:for-each>

      <fo:block id="end-of-doc"/>

    </fo:flow>
  </fo:page-sequence>

</fo:root>

</xsl:template>

</xsl:stylesheet>