import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from datatopdf import DataToPdf
import os

def createNewReport(reached, unreached, data, filename): 
    doc = SimpleDocTemplate(filename,pagesize=A4,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    logo = "images/figure.png"
    chart_min = "images/fig_min.png"
    chart_max = "images/fig_max.png"
    map_w = "images/ip_map_w.png"
    map_o = "images/ip_map_o.png"
    map_total = "images/total_ip_map.png"
     
    formatted_time = time.ctime()

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    #Print time
    ptext = '<font size=8>%s</font>' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 0.2*cm))

    ###Print stat analyze
    ##Percentage stats
    ptext = "<font size=14>Misc-Stats: </font>"
    Story.append(Paragraph(ptext, styles["Heading1"]))
    ptext = "<font size=12>Totally pinged IP-Adresses: " + str(reached + unreached) + "</font>"
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = "<font size=12>Responding IP-Adresses: " + str(reached) + "</font>"
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = "<font size=12>Not responding IP-Adresses: " + str(unreached) + "</font>"
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = "<font size=12>Percentage: " + str(round((reached/(unreached+reached))*100, 3)) + "</font>"
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ##Time analysis
    #Average time
    times = []
    for i in data:
        if i["restime"] != "ris":
            times.append(int(i["restime"]))
    avgtime = sum(times) / float(len(times))
    ptext = "<font size=20>Time-Stats:</font>"
    Story.append(Paragraph(ptext, styles["Heading1"]))
    Story.append(Spacer(1, 12))
    ptext = "<font size=14>The average response time was " + str(round(avgtime,2)) + "</font>"
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    #Response time per country
    ptext = "<font size=18>Average response time for every country (ASCENDING):</font>"
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    im = Image(chart_min, 6.4*inch*0.6, 4.8*inch*0.6)
    Story.append(im)
    ptext = "<font size=18>Average response time for every country (DESCENDING):</font>"
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    im = Image(chart_max, 6.4*inch*0.6, 4.8*inch*0.6)
    Story.append(im)

    #Print Header and BarChart
    ptext = "<font size=20>The dispersal of the responding IPs to the countrys:</font>"
    Story.append(Paragraph(ptext, styles["Heading1"]))
    Story.append(Spacer(1, 12))
    im = Image(logo, 6.4*inch, 4.8*inch)
    Story.append(im)
    #New Page
    Story.append(PageBreak())

    #Print map of current result
    ptext = "<font size=20>The locations of every IP founded in this result:</font>"
    Story.append(Paragraph(ptext, styles["Heading1"]))
    Story.append(Spacer(1, 12))
    Story.append(Image(map_w, 17.28*cm, 9.72*cm))
    Story.append(Spacer(1, 12))
    Story.append(Image(map_o, 17.28*cm, 9.72*cm))
    #New Page
    Story.append(PageBreak())

    #Print map of total result
    ptext = "<font size=20>The locations of every IP ever founded:</font>"
    Story.append(Paragraph(ptext, styles["Heading1"]))
    Story.append(Spacer(1, 12))
    Story.append(Image(map_total, 17.28*cm, 9.72*cm))
    #New Page
    Story.append(PageBreak())

    #Add table with the IP-Informations
    fields = (
        ('as', 'Name'),
        ('city', 'City'),
        ('country', 'Country'),
        ('query', 'IP'),
        ('regionName', 'Region'),
        ('zip', 'ZIP-Code'),
    )
    table = DataToPdf(fields, data, sort_by=('query', 'DESC'),
                    title='Informations about the IP-Adresses')
    Story.append(table.export())


    doc.build(Story)



if __name__ == '__main__':
    print("Module")