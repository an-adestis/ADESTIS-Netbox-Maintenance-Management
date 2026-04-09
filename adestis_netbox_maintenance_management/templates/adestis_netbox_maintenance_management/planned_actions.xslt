<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format">

  <xsl:output method="xml" indent="yes"/>

  <!-- ROOT MATCH (funktioniert für beide Varianten indirekt über apply-templates) -->
  <xsl:template match="/">

    <xsl:apply-templates select="planned-actions | planned_actions"/>

  </xsl:template>

  <!-- HAUPT-TEMPLATE -->
  <xsl:template match="planned-actions | planned_actions">

    <!-- Safe Next Due Date -->
    <xsl:variable name="nextDueDate"
      select="(group[1]/next_due_date | group[1]/@due-date)[1]"/>

    <fo:root>
      <fo:layout-master-set>
        <fo:simple-page-master master-name="A4"
            page-height="29.7cm"
            page-width="21cm"
            margin="2cm">
          <fo:region-body margin-top="3cm"/>
          <fo:region-before extent="3cm"/>
        </fo:simple-page-master>
      </fo:layout-master-set>

      <fo:page-sequence master-reference="A4">

        <!-- HEADER (jede Seite) -->
        <fo:static-content flow-name="xsl-region-before">
          <fo:block font-size="16pt" font-weight="bold" color="#007b8a">
            Planned Actions
          </fo:block>

          <fo:block font-size="10pt" color="#333333">
            Datum:
            <xsl:choose>
              <xsl:when test="$nextDueDate">
                <xsl:value-of select="$nextDueDate"/>
              </xsl:when>
              <xsl:otherwise>-</xsl:otherwise>
            </xsl:choose>
          </fo:block>

          <fo:block border-bottom="1pt solid #007b8a" margin-top="4pt"/>
        </fo:static-content>

        <!-- CONTENT -->
        <fo:flow flow-name="xsl-region-body" font-family="Helvetica">

          <fo:block id="last-page-marker"/>

          <fo:table table-layout="fixed" width="100%" border="0.5pt solid #007b8a" margin-top="10pt">

            <!-- HEADER -->
            <fo:table-header>
              <fo:table-row background-color="#007b8a" color="white" font-weight="bold">
                <fo:table-cell padding="4pt"><fo:block>Startzeit</fo:block></fo:table-cell>
                <fo:table-cell padding="4pt"><fo:block>Endzeit</fo:block></fo:table-cell>
                <fo:table-cell padding="4pt"><fo:block>Maintenance Action</fo:block></fo:table-cell>
              </fo:table-row>
            </fo:table-header>

            <fo:table-body>

              <!-- ACTIONS -->
              <xsl:for-each select="group/maintenance_action">

                <!-- MAIN ROW -->
                <fo:table-row background-color="#e6f3f5" font-weight="bold">

                  <fo:table-cell padding="4pt" border="0.5pt solid #007b8a">
                    <fo:block>
                      <xsl:choose>
                        <xsl:when test="start_time">
                          <xsl:value-of select="start_time"/>
                        </xsl:when>
                        <xsl:otherwise>-</xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>

                  <fo:table-cell padding="4pt" border="0.5pt solid #007b8a">
                    <fo:block>
                      <xsl:choose>
                        <xsl:when test="end_time">
                          <xsl:value-of select="end_time"/>
                        </xsl:when>
                        <xsl:otherwise>-</xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>

                  <fo:table-cell padding="4pt" border="0.5pt solid #007b8a">
                    <fo:block>
                      <xsl:choose>
                        <xsl:when test="name">
                          <xsl:value-of select="name"/>
                        </xsl:when>
                        <xsl:when test="maintenance_action_name">
                          <xsl:value-of select="maintenance_action_name"/>
                        </xsl:when>
                        <xsl:otherwise>-</xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>

                </fo:table-row>

                <!-- DETAILS -->
                <fo:table-row>
                  <fo:table-cell number-columns-spanned="3"
                                  padding="6pt"
                                  border="0.5pt solid #007b8a"
                                  background-color="#f9f9f9">

                    <!-- verhindert FOP Crash -->
                    <fo:block/>

                    <!-- VMs -->
                    <xsl:if test="vms/vm">
                      <fo:block font-weight="bold" background-color="#eeeeee" padding="3pt" margin-bottom="2pt">
                        VM
                      </fo:block>

                      <fo:table width="100%" border="0.5pt solid #999999">
                        <fo:table-header>
                          <fo:table-row background-color="#dddddd" font-weight="bold">
                            <fo:table-cell padding="3pt"><fo:block>Name</fo:block></fo:table-cell>
                            <fo:table-cell padding="3pt"><fo:block>Info</fo:block></fo:table-cell>
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

                    <!-- DEVICES -->
                    <xsl:if test="devices/device">
                      <fo:block font-weight="bold" background-color="#eeeeee" padding="3pt" margin-top="6pt" margin-bottom="2pt">
                        Device
                      </fo:block>

                      <fo:table width="100%" border="0.5pt solid #999999">
                        <fo:table-header>
                          <fo:table-row background-color="#dddddd" font-weight="bold">
                            <fo:table-cell padding="3pt"><fo:block>Name</fo:block></fo:table-cell>
                            <fo:table-cell padding="3pt"><fo:block>Info</fo:block></fo:table-cell>
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

          <!-- FOOTER -->
          <fo:block font-size="8pt" color="#666666" margin-top="20pt" text-align="right">
            Seite <fo:page-number/> /
            <fo:page-number-citation-last ref-id="last-page-marker"/>
          </fo:block>

        </fo:flow>
      </fo:page-sequence>
    </fo:root>

  </xsl:template>

</xsl:stylesheet>