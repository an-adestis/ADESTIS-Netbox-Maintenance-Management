<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

  <xsl:output method="xml" indent="yes"/>

  <xsl:template match="/">
    <xsl:apply-templates select="planned-actions | planned_actions"/>
  </xsl:template>

  <xsl:template match="planned-actions | planned_actions">

    <fo:root>
      <fo:layout-master-set>
        <fo:simple-page-master master-name="A4"
            page-height="29.7cm"
            page-width="21cm"
            margin="2cm">
          <fo:region-body margin-top="3.5cm" margin-bottom="1.5cm"/>
          <fo:region-before extent="3.5cm"/>
          <fo:region-after extent="1.5cm"/>
        </fo:simple-page-master>
      </fo:layout-master-set>

      <fo:page-sequence master-reference="A4">

        <!-- HEADER -->
        <fo:static-content flow-name="xsl-region-before">
          <fo:block font-size="22pt" font-weight="bold" color="#E5133A"
                    font-family="Helvetica" margin-bottom="4pt">
            Planned Actions
          </fo:block>
          <fo:block font-size="10pt" color="#333333" font-family="Helvetica" margin-bottom="6pt">
            Datum: <xsl:value-of select="group[1]/next_due_date"/>
          </fo:block>
          <fo:block border-bottom="2pt solid #E5133A"/>
        </fo:static-content>

        <!-- FOOTER -->
        <fo:static-content flow-name="xsl-region-after">
          <fo:block border-top="1pt solid #cccccc" margin-bottom="4pt"/>
          <fo:table table-layout="fixed" width="100%">
            <fo:table-column column-width="proportional-column-width(1)"/>
            <fo:table-column column-width="proportional-column-width(1)"/>
            <fo:table-body>
              <fo:table-row>
                <fo:table-cell>
                  <fo:block font-size="8pt" color="#666666" font-family="Helvetica">
                    <xsl:value-of select="group[1]/next_due_date"/>
                  </fo:block>
                </fo:table-cell>
                <fo:table-cell text-align="right">
                  <fo:block font-size="8pt" color="#666666" font-family="Helvetica">
                    Seite <fo:page-number/> / <fo:page-number-citation-last ref-id="last-block"/>
                  </fo:block>
                </fo:table-cell>
              </fo:table-row>
            </fo:table-body>
          </fo:table>
        </fo:static-content>

        <!-- HAUPTINHALT -->
        <fo:flow flow-name="xsl-region-body" font-family="Helvetica" font-size="9pt"
                 color="#333333">

          <fo:block id="last-block"/>

          <fo:table table-layout="fixed" width="100%"
                    border="0.5pt solid #cccccc">

            <fo:table-column column-width="3cm"/>
            <fo:table-column column-width="3cm"/>
            <fo:table-column column-width="proportional-column-width(1)"/>

            <fo:table-header>
              <fo:table-row background-color="#E5133A" color="white" font-weight="bold">
                <fo:table-cell padding="5pt" border="0.5pt solid #cccccc">
                  <fo:block>Startzeit</fo:block>
                </fo:table-cell>
                <fo:table-cell padding="5pt" border="0.5pt solid #cccccc">
                  <fo:block>Endzeit</fo:block>
                </fo:table-cell>
                <fo:table-cell padding="5pt" border="0.5pt solid #cccccc">
                  <fo:block>Maintenance Action</fo:block>
                </fo:table-cell>
              </fo:table-row>
            </fo:table-header>

            <fo:table-body>
              <xsl:choose>
                <xsl:when test="group/maintenance_action">
                  <xsl:for-each select="group/maintenance_action">

                    <fo:table-row font-weight="bold"
                                  background-color="#fde8ec"
                                  keep-with-next.within-page="always">
                      <fo:table-cell padding="5pt" border="0.5pt solid #cccccc">
                        <fo:block color="#333333">
                          <xsl:choose>
                            <xsl:when test="normalize-space(start_time) != ''">
                              <xsl:value-of select="start_time"/>
                            </xsl:when>
                            <xsl:otherwise>-</xsl:otherwise>
                          </xsl:choose>
                        </fo:block>
                      </fo:table-cell>
                      <fo:table-cell padding="5pt" border="0.5pt solid #cccccc">
                        <fo:block color="#333333">
                          <xsl:choose>
                            <xsl:when test="normalize-space(end_time) != ''">
                              <xsl:value-of select="end_time"/>
                            </xsl:when>
                            <xsl:otherwise>-</xsl:otherwise>
                          </xsl:choose>
                        </fo:block>
                      </fo:table-cell>
                      <fo:table-cell padding="5pt" border="0.5pt solid #cccccc">
                        <fo:block color="#333333">
                          <xsl:choose>
                            <xsl:when test="normalize-space(name) != ''">
                              <xsl:value-of select="name"/>
                            </xsl:when>
                            <xsl:otherwise>-</xsl:otherwise>
                          </xsl:choose>
                        </fo:block>
                      </fo:table-cell>
                    </fo:table-row>

                    <!-- DETAILZEILE -->
                    <fo:table-row>
                      <fo:table-cell number-columns-spanned="3"
                                     padding="8pt"
                                     border="0.5pt solid #cccccc"
                                     border-top="0pt">
                        <fo:block/>

                        <!-- Comments -->
                        <xsl:if test="normalize-space(comments) != ''">
                          <fo:block font-style="italic" color="#666666" margin-bottom="8pt">
                            <xsl:value-of select="comments"/>
                          </fo:block>
                        </xsl:if>

                        <!-- VMs -->
                        <xsl:if test="vms/vm">
                          <fo:block font-weight="bold" color="#333333"
                                    border-bottom="1pt solid #cccccc"
                                    padding-bottom="2pt" margin-bottom="4pt">
                            VM
                          </fo:block>
                          <fo:table width="100%" border="0.5pt solid #cccccc">
                            <fo:table-column column-width="proportional-column-width(1)"/>
                            <fo:table-column column-width="proportional-column-width(2)"/>
                            <fo:table-header>
                              <fo:table-row background-color="#f5f5f5" font-weight="bold">
                                <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                  <fo:block>Name</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                  <fo:block>Info</fo:block>
                                </fo:table-cell>
                              </fo:table-row>
                            </fo:table-header>
                            <fo:table-body>
                              <xsl:for-each select="vms/vm">
                                <fo:table-row>
                                  <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                    <fo:block><xsl:value-of select="name"/></fo:block>
                                  </fo:table-cell>
                                  <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                    <fo:block>
                                      <xsl:choose>
                                        <xsl:when test="normalize-space(comment) != ''">
                                          <xsl:value-of select="comment"/>
                                        </xsl:when>
                                        <xsl:otherwise>-</xsl:otherwise>
                                      </xsl:choose>
                                    </fo:block>
                                  </fo:table-cell>
                                </fo:table-row>
                              </xsl:for-each>
                            </fo:table-body>
                          </fo:table>
                        </xsl:if>

                        <!-- Devices -->
                        <xsl:if test="devices/device">
                          <fo:block font-weight="bold" color="#333333"
                                    border-bottom="1pt solid #cccccc"
                                    padding-bottom="2pt" margin-top="10pt" margin-bottom="4pt">
                            Device
                          </fo:block>
                          <fo:table width="100%" border="0.5pt solid #cccccc">
                            <fo:table-column column-width="proportional-column-width(1)"/>
                            <fo:table-column column-width="proportional-column-width(2)"/>
                            <fo:table-header>
                              <fo:table-row background-color="#f5f5f5" font-weight="bold">
                                <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                  <fo:block>Name</fo:block>
                                </fo:table-cell>
                                <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                  <fo:block>Info</fo:block>
                                </fo:table-cell>
                              </fo:table-row>
                            </fo:table-header>
                            <fo:table-body>
                              <xsl:for-each select="devices/device">
                                <fo:table-row>
                                  <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                    <fo:block><xsl:value-of select="name"/></fo:block>
                                  </fo:table-cell>
                                  <fo:table-cell padding="3pt" border="0.5pt solid #cccccc">
                                    <fo:block>
                                      <xsl:choose>
                                        <xsl:when test="normalize-space(comment) != ''">
                                          <xsl:value-of select="comment"/>
                                        </xsl:when>
                                        <xsl:otherwise>-</xsl:otherwise>
                                      </xsl:choose>
                                    </fo:block>
                                  </fo:table-cell>
                                </fo:table-row>
                              </xsl:for-each>
                            </fo:table-body>
                          </fo:table>
                        </xsl:if>

                        <!-- Weder VMs noch Devices -->
                        <xsl:if test="not(vms/vm) and not(devices/device)">
                          <fo:block color="#999999" font-style="italic">
                            Keine VMs oder Devices zugewiesen.
                          </fo:block>
                        </xsl:if>

                      </fo:table-cell>
                    </fo:table-row>

                  </xsl:for-each>
                </xsl:when>

                <xsl:otherwise>
                  <fo:table-row>
                    <fo:table-cell number-columns-spanned="3" padding="8pt">
                      <fo:block color="#999999" font-style="italic" text-align="center">
                        Keine geplanten Aktionen vorhanden.
                      </fo:block>
                    </fo:table-cell>
                  </fo:table-row>
                </xsl:otherwise>

              </xsl:choose>
            </fo:table-body>
          </fo:table>

        </fo:flow>
      </fo:page-sequence>
    </fo:root>

  </xsl:template>

</xsl:stylesheet>