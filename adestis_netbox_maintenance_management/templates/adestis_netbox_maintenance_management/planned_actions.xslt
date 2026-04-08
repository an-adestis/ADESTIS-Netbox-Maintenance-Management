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

          <!-- Marker für Seitenzahl -->
          <fo:block id="last-page-marker"/>

          <!-- Titel -->
          <fo:block font-size="16pt" font-weight="bold" space-after="10pt" color="#007b8a">
            Planned Actions
          </fo:block>

          <!-- Datum / Due Date -->
          <fo:block font-size="10pt" space-after="8pt" color="#333333">
            Due Date: <xsl:value-of select="group/@due-date"/>
          </fo:block>

          <!-- Haupttabelle -->
          <fo:table table-layout="fixed" width="100%" border="0.5pt solid #007b8a">
            <fo:table-header>
              <fo:table-row background-color="#007b8a" color="white" font-weight="bold">
                <fo:table-cell padding="4pt"><fo:block>Startzeit</fo:block></fo:table-cell>
                <fo:table-cell padding="4pt"><fo:block>Endzeit</fo:block></fo:table-cell>
                <fo:table-cell padding="4pt"><fo:block>Maintenance Action</fo:block></fo:table-cell>
              </fo:table-row>
            </fo:table-header>

            <fo:table-body>
              <xsl:for-each select="group/action">

                <!-- Hauptzeile -->
                <fo:table-row background-color="#e6f3f5" font-weight="bold">
                  <fo:table-cell padding="4pt" border="0.5pt solid #007b8a">
                    <fo:block><xsl:value-of select="start-time"/></fo:block>
                  </fo:table-cell>

                  <fo:table-cell padding="4pt" border="0.5pt solid #007b8a">
                    <fo:block><xsl:value-of select="end-time"/></fo:block>
                  </fo:table-cell>

                  <fo:table-cell padding="4pt" border="0.5pt solid #007b8a">
                    <fo:block><xsl:value-of select="name"/></fo:block>
                  </fo:table-cell>
                </fo:table-row>

                <!-- Details: VMs -->
                <fo:table-row>
                  <fo:table-cell number-columns-spanned="3"
                                  padding="6pt"
                                  border="0.5pt solid #007b8a"
                                  background-color="#f9f9f9">

                    <!-- VMs -->
                    <xsl:if test="vms/vm">
                      <fo:block font-weight="bold" background-color="#eeeeee" padding="3pt" margin-bottom="2pt">VM</fo:block>
                      <fo:table width="100%" border="0.5pt solid #999999">
                        <fo:table-header>
                          <fo:table-row background-color="#dddddd" font-weight="bold">
                            <fo:table-cell padding="3pt"><fo:block>Name</fo:block></fo:table-cell>
                            <fo:table-cell padding="3pt"><fo:block>Comment</fo:block></fo:table-cell>
                          </fo:table-row>
                        </fo:table-header>
                        <fo:table-body>
                          <xsl:for-each select="vms/vm">
                            <fo:table-row>
                              <fo:table-cell padding="3pt" border="0.5pt solid #999999">
                                <fo:block>
                                  <xsl:value-of select="name"/>
                                  <xsl:if test="not(name)">-</xsl:if>
                                </fo:block>
                              </fo:table-cell>
                              <fo:table-cell padding="3pt" border="0.5pt solid #999999">
                                <fo:block>
                                  <xsl:value-of select="comment"/>
                                  <xsl:if test="not(comment)">-</xsl:if>
                                </fo:block>
                              </fo:table-cell>
                            </fo:table-row>
                          </xsl:for-each>
                        </fo:table-body>
                      </fo:table>
                    </xsl:if>

                    <!-- Devices -->
                    <xsl:if test="devices/device">
                      <fo:block font-weight="bold" background-color="#eeeeee" padding="3pt" margin-top="6pt" margin-bottom="2pt">Device</fo:block>
                      <fo:table width="100%" border="0.5pt solid #999999">
                        <fo:table-header>
                          <fo:table-row background-color="#dddddd" font-weight="bold">
                            <fo:table-cell padding="3pt"><fo:block>Name</fo:block></fo:table-cell>
                            <fo:table-cell padding="3pt"><fo:block>Comment</fo:block></fo:table-cell>
                          </fo:table-row>
                        </fo:table-header>
                        <fo:table-body>
                          <xsl:for-each select="devices/device">
                            <fo:table-row>
                              <fo:table-cell padding="3pt" border="0.5pt solid #999999">
                                <fo:block>
                                  <xsl:value-of select="name"/>
                                  <xsl:if test="not(name)">-</xsl:if>
                                </fo:block>
                              </fo:table-cell>
                              <fo:table-cell padding="3pt" border="0.5pt solid #999999">
                                <fo:block>
                                  <xsl:value-of select="comment"/>
                                  <xsl:if test="not(comment)">-</xsl:if>
                                </fo:block>
                              </fo:table-cell>
                            </fo:table-row>
                          </xsl:for-each>
                        </fo:table-body>
                      </fo:table>
                    </xsl:if>

                  </fo:table-cell>
                </fo:table-row>

              </xsl:for-each>
            </fo:table-body>
          </fo:table>

          <!-- Footer -->
          <fo:block font-size="8pt" color="#666666" margin-top="20pt" text-align="right">
            Seite <fo:page-number/> / 
            <fo:page-number-citation-last ref-id="last-page-marker"/>
          </fo:block>

        </fo:flow>
      </fo:page-sequence>
    </fo:root>

  </xsl:template>

</xsl:stylesheet>