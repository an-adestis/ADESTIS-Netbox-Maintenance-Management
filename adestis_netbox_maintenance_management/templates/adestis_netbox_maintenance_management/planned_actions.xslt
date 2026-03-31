<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

  <xsl:output method="xml" indent="yes"/>

  <xsl:template match="/planned-actions">

    <fo:root>
      <fo:layout-master-set>
        <fo:simple-page-master master-name="A4"
            page-height="29.7cm"
            page-width="21cm"
            margin="2cm">
          <fo:region-body/>
        </fo:simple-page-master>
      </fo:layout-master-set>

      <fo:page-sequence master-reference="A4">
        <fo:flow flow-name="xsl-region-body" font-family="Helvetica">

          <!-- Marker für letzte Seite -->
          <fo:block id="last-page-marker"/>

          <fo:block font-size="16pt" font-weight="bold" space-after="10pt" color="#a9c5d3">
            Planned Actions
          </fo:block>

          <fo:block font-size="10pt" space-after="5pt" color="#a9c5d3">
            Datum: <xsl:value-of select="group/@date"/>
          </fo:block>

          <fo:table table-layout="fixed" width="100%" border="0.5pt solid #007b8a" >

            <!-- Header -->
            <fo:table-header>
              <fo:table-row background-color="#007b8a" color="white" font-weight="bold" font-size="9pt">
                <fo:table-cell padding="3pt"><fo:block>Startzeit</fo:block></fo:table-cell>
                <fo:table-cell padding="3pt"><fo:block>Endzeit</fo:block></fo:table-cell>
                <fo:table-cell padding="3pt"><fo:block>Maintenance Action</fo:block></fo:table-cell>
              </fo:table-row>
            </fo:table-header>

            <fo:table-body>
              <xsl:for-each select="group/action">
                <!-- Erste Zeile: Hauptdaten -->
                <fo:table-row background-color="#007b8a" color="white" font-weight="bold" font-size="9pt">
                  <fo:table-cell padding="3pt" border="0.5pt solid #007b8a">
                    <fo:block><xsl:value-of select="start-time"/></fo:block>
                  </fo:table-cell>
                  <fo:table-cell padding="3pt" border="0.5pt solid #007b8a">
                    <fo:block><xsl:value-of select="end-time"/></fo:block>
                  </fo:table-cell>
                  <fo:table-cell padding="3pt" border="0.5pt solid #007b8a">
                    <fo:block><xsl:value-of select="maintenance-action-name"/></fo:block>
                  </fo:table-cell>
                </fo:table-row>

                <!-- Zweite Zeile: Details -->
                <fo:table-row>
                  <fo:table-cell padding="3pt" number-columns-spanned="3" border="0.5pt solid #007b8a" background-color="#1a1a1a" color="white">
                    <fo:block>
                      <xsl:if test="comments">
                        <fo:block font-weight="bold" margin-bottom="4pt">Kommentare:</fo:block>
                        <fo:block margin-bottom="10pt" linefeed-treatment="preserve"><xsl:value-of select="comments"/></fo:block>
                      </xsl:if>

                      <!-- VM-Tabelle -->
                      <xsl:if test="vm-table/vm">
                        <fo:block font-weight="bold" background-color="#eeeeee" color="black" padding="3pt" margin-bottom="4pt">VM</fo:block>
                        <fo:table table-layout="fixed" width="100%">
                          <fo:table-column column-width="50%"/>
                          <fo:table-column column-width="50%"/>
                          <fo:table-header>
                            <fo:table-row background-color="#cccccc" font-weight="bold">
                              <fo:table-cell padding="3pt" border="1pt solid #666666"><fo:block>VM</fo:block></fo:table-cell>
                              <fo:table-cell padding="3pt" border="1pt solid #666666"><fo:block>Info</fo:block></fo:table-cell>
                            </fo:table-row>
                          </fo:table-header>
                          <fo:table-body>
                            <xsl:for-each select="vm-table/vm">
                              <fo:table-row>
                                <xsl:attribute name="background-color">
                                  <xsl:choose>
                                    <xsl:when test="position() mod 2 = 1">#333333</xsl:when>
                                    <xsl:otherwise>#444444</xsl:otherwise>
                                  </xsl:choose>
                                </xsl:attribute>
                                <fo:table-cell padding="3pt" border="1pt solid #666666">
                                  <fo:block><xsl:value-of select="vm-name"/></fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding="3pt" border="1pt solid #666666">
                                  <fo:block><xsl:value-of select="vm-comment"/></fo:block>
                                </fo:table-cell>
                              </fo:table-row>
                            </xsl:for-each>
                          </fo:table-body>
                        </fo:table>
                      </xsl:if>

                      <!-- Device-Tabelle -->
                      <xsl:if test="device-table/device">
                        <fo:block font-weight="bold" background-color="#eeeeee" color="black" padding="3pt" margin-bottom="4pt">Device</fo:block>
                        <fo:table table-layout="fixed" width="100%">
                          <fo:table-column column-width="50%"/>
                          <fo:table-column column-width="50%"/>
                          <fo:table-header>
                            <fo:table-row background-color="#cccccc" font-weight="bold">
                              <fo:table-cell padding="3pt" border="1pt solid #666666"><fo:block>Device</fo:block></fo:table-cell>
                              <fo:table-cell padding="3pt" border="1pt solid #666666"><fo:block>Info</fo:block></fo:table-cell>
                            </fo:table-row>
                          </fo:table-header>
                          <fo:table-body>
                            <xsl:for-each select="device-table/device">
                              <fo:table-row>
                                <xsl:attribute name="background-color">
                                  <xsl:choose>
                                    <xsl:when test="position() mod 2 = 1">#333333</xsl:when>
                                    <xsl:otherwise>#444444</xsl:otherwise>
                                  </xsl:choose>
                                </xsl:attribute>
                                <fo:table-cell padding="3pt" border="1pt solid #666666">
                                  <fo:block><xsl:value-of select="device-name"/></fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding="3pt" border="1pt solid #666666">
                                  <fo:block><xsl:value-of select="vm-comment"/></fo:block>
                                </fo:table-cell>
                              </fo:table-row>
                            </xsl:for-each>
                          </fo:table-body>
                        </fo:table>
                      </xsl:if>

                    </fo:block>
                  </fo:table-cell>
                </fo:table-row>
              </xsl:for-each>

            </fo:table-body>

          </fo:table>

          <!-- Seitenzahl korrekt mit ref-id -->
          <fo:block font-size="8pt" color="#666666" margin-top="20pt" text-align="right">
            Seite <fo:page-number/> / <fo:page-number-citation-last ref-id="last-page-marker"/>
          </fo:block>

          <fo:block font-size="8pt" color="#666666" margin-top="10pt" text-align="left">
            <xsl:value-of select="/planned-actions/pdf-created-date"/>
          </fo:block>

          <fo:block font-size="6pt" color="#666666" margin-top="10pt" text-align="right">
            ADESTIS Logo
          </fo:block>

        </fo:flow>
      </fo:page-sequence>
    </fo:root>
  </xsl:template>

</xsl:stylesheet>