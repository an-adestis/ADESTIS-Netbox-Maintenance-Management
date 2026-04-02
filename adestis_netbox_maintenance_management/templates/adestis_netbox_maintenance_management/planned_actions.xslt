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
        <fo:flow flow-name="xsl-region-body"
                 font-family="Helvetica, Arial, sans-serif"
                 font-size="10pt"
                 color="#333333">

          <fo:block id="last-page-marker"/>

          <!-- Titel -->
          <fo:block font-size="18pt"
                    font-weight="bold"
                    space-after="10pt"
                    color="#36ddabff">
            Planned Actions
          </fo:block>

          <!-- Datum -->
          <fo:block font-size="12pt"
                    space-after="15pt">
            Datum: <xsl:value-of select="group/@date"/>
          </fo:block>

          <!-- HAUPTTABELLE -->
          <fo:table table-layout="fixed"
                    width="100%"
                    border="0.5pt solid #007b8a">

            <fo:table-column column-width="3cm"/>
            <fo:table-column column-width="3cm"/>
            <fo:table-column column-width="14cm"/>

            <!-- HEADER -->
            <fo:table-header>
              <fo:table-row background-color="#007b8a"
                            color="white"
                            font-weight="bold">
                <fo:table-cell padding="5pt">
                  <fo:block>Startzeit</fo:block>
                </fo:table-cell>
                <fo:table-cell padding="5pt">
                  <fo:block>Endzeit</fo:block>
                </fo:table-cell>
                <fo:table-cell padding="5pt">
                  <fo:block>Maintenance Action</fo:block>
                </fo:table-cell>
              </fo:table-row>
            </fo:table-header>

            <!-- BODY -->
            <fo:table-body>
              <xsl:for-each select="group/action">

  <!-- ZEILE -->
  <fo:table-row background-color="#007b8a" color="white" font-weight="bold">

    <fo:table-cell padding="5pt">
      <fo:block>
        <xsl:value-of select="start_time"/>
      </fo:block>
    </fo:table-cell>

    <fo:table-cell padding="5pt">
      <fo:block>
        <xsl:value-of select="end_time"/>
      </fo:block>
    </fo:table-cell>

    <fo:table-cell padding="5pt">
      <fo:block>
        <!-- ❗ ALLE Maintenance Actions -->
        <xsl:for-each select="../maintenance_action">
          <xsl:value-of select="name"/>
          <xsl:if test="position() != last()">, </xsl:if>
        </xsl:for-each>
      </fo:block>
    </fo:table-cell>

  </fo:table-row>

  <!-- DETAILS -->
  <fo:table-row background-color="#1b1b1b" color="white" font-size="8pt">
    <fo:table-cell number-columns-spanned="3" padding="5pt">

      <!-- VMs -->
      <xsl:if test="../virtual_machine">
        <fo:block font-weight="bold" space-after="4pt">VMs:</fo:block>

        <xsl:for-each select="../virtual_machine">
          <fo:block>
            • <xsl:value-of select="name"/>
          </fo:block>
        </xsl:for-each>
      </xsl:if>

      <!-- Devices -->
      <xsl:if test="../device">
        <fo:block font-weight="bold" space-before="6pt" space-after="4pt">Devices:</fo:block>

        <xsl:for-each select="../device">
          <fo:block>
            • <xsl:value-of select="name"/>
          </fo:block>
        </xsl:for-each>
      </xsl:if>

    </fo:table-cell>
  </fo:table-row>

</xsl:for-each>
            </fo:table-body>

          </fo:table>

          <!-- Footer -->
          <fo:block font-size="8pt"
                    color="#666666"
                    margin-top="20pt"
                    text-align="right">
            Seite <fo:page-number/> /
            <fo:page-number-citation-last ref-id="last-page-marker"/>
          </fo:block>

          <fo:block font-size="8pt"
                    margin-top="10pt">
            <xsl:value-of select="/planned-actions/pdf-created-date"/>
          </fo:block>

        </fo:flow>
      </fo:page-sequence>
    </fo:root>

  </xsl:template>
</xsl:stylesheet>