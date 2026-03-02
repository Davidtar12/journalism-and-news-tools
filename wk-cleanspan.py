# -*- coding: utf-8 -*-
import re

def remove_span_tags(html_content):
    """
    Remove all <span> and </span> tags from the HTML content while keeping other tags intact.

    Args:
    html_content (str): The HTML content from which <span> tags need to be removed.

    Returns:
    str: The HTML content with <span> tags removed.
    """
    # Remove <span> and </span> tags
    clean_content = re.sub(r'<\s*span[^>]*>|<\s*/\s*span\s*>', '', html_content)

    return clean_content

# Example usage with a long HTML document
html_input = """
<span style="font-weight: 400;">Comunidades indígenas de la Amazonía ecuatoriana denunciaron que, al menos, seis derrames petroleros ocurridos entre junio y agosto de 2024, provocaron la contaminación de la Comuna San Antonio, en la parroquia Pompeya, ubicada en el cantón Joya de los Sachas, Orellana. </span>

<span style="font-weight: 400;">La comunidad Nueva Providencia también se ha visto afectada por los derrames ocurridos en los últimos meses. Los pobladores aseguran que se contaminaron ríos, como el Intillama, el Shipati, el Jivino y el Napo, lo que ha perjudicado la obtención de agua pura, así como las actividades de pesca.</span>

<span style="font-weight: 400;">Los pobladores señalan que han pedido información sobre la magnitud y el volumen de los derrames, así como las acciones de  limpieza. “Pero no nos han dado la información de limpieza, remediación, ni compensación”, dice Leandro Tapuy, presidente de la comunidad kichwa Río Intillama, una de las afectadas.</span>

<span style="font-weight: 400;">Thomas Worsdell, coordinador de monitoreo de campo de la organización ambiental Amazon Frontlines y que ha documentado en terreno los daños ambientales denunciados, explicó que los derrames de petróleo iniciaron en mayo de 2024 en el cantón Joya de los Sachas, en la provincia amazónica de Orellana. “Entre el 27 de mayo y el 17 de junio hubo al menos cuatro derrames en tres secciones de la tubería”, asegura. </span>

[caption id="attachment_254054" align="alignnone" width="1920"]<img class="size-full wp-image-254054" src="https://imgs.mongabay.com/wp-content/uploads/sites/25/2024/08/30211016/IMG_7107-2.jpg" alt="Derrame petrolero en Orellana, Ecuador sucedido en 2024. Foto: Amazon Frontlines." width="1920" height="1440" /> Derrame petrolero en Orellana, Ecuador sucedido en 2024. Foto: Amazon Frontlines.[/caption]

<span style="font-weight: 400;">En las redes sociales Twitter y Facebook, las comunidades denunciaron nuevos derrames petroleros ocurridos  a finales de agosto. Los habitantes, además, señalan que los derrames se han presentado en inmediaciones o cercanías del Parque Nacional Yasuní, donde el pueblo ecuatoriano votó para prohibir </span><a href="https://es.mongabay.com/2024/08/ecuador-economistas-proponen-alternativas-dejar-de-explotar-petroleo-yasuni/"><span style="font-weight: 400;">la extracción de crudo</span></a><span style="font-weight: 400;">, pero el gobierno aún no lo aplica.</span>

<b>La situación no es nueva</b>

<span style="font-weight: 400;">“No son las primeras veces que sucede, la tubería está vieja y dañada. Hay derrames todo el tiempo, pero estos últimos, ocurridos entre mayo y junio, fueron más grandes”, asegura Worsdell. Agrega que también hubo derrames al otro lado del río Napo, en un pozo de Repsol, en el Bloque 16. Hay múltiples cuerpos de agua afectados, entre estos el río Intillama y el Shipati, los cuales desembocan en el Napo. Un comunicado menciona la estación Yananquincha y la estación central CPF bloque 15.</span>

<span style="font-weight: 400;">Wilmer Lucitante, líder comunitario de la nacionalidad Cofán de la Amazonía de Ecuador y parte de la Asociación de Productores Audiovisuales de las Nacionalidades y Pueblos de Sucumbios Ecuador, explica que las empresas no actuaron de manera inmediata frente a los derrames que se registraron el 8 de junio. “A partir del 11 pusieron unas salchichas —barreras flotantes temporales que se utilizan que absorben el petróleo en el agua que parecen “salchichas”— no se la palabra técnica en castellano pero con la lluvia se derramó el petróleo hacia el río Napo y contaminó las quebradas, el río Shipati y todas las comunidades kichwa de la ribera: Intillama, Puerto Providencia, bueno un montón”. </span>

[caption id="attachment_254055" align="alignnone" width="1920"]<img class="size-full wp-image-254055" src="https://imgs.mongabay.com/wp-content/uploads/sites/25/2024/08/30211218/IMG_7133-2.jpg" alt="Así se ven los derrames petroleros que afectaron la provincia de Orellana en 2024 en la Amazonía ecuatoriana. Foto: Amazon Frontlines." width="1920" height="1440" /> Así se ven los derrames petroleros que afectaron la provincia de Orellana en 2024 en la Amazonía ecuatoriana. Foto: Amazon Frontlines.[/caption]

<span style="font-weight: 400;">Tras múltiples quejas en redes sociales y preguntas de periodistas al Ministerio del Ambiente, la entidad publicó un comunicado sobre los derrames sucedidos en la provincia de Orellana, en particular en el Bloque 67-67 Iro Tivacuno. La dependencia señaló que conforme a la normativa, le solicitaron a Petroecuador implementar un plan emergente y “medidas de contingencia”, que incluyeran barreras de contención, pero que debido a las lluvias, el agua con crudo se desbordó, llegando al río Napo. En el boletín aseguran que supervisarán la situación.</span>

<span style="font-weight: 400;">No obstante, las personas consultadas por Mongabay Latam, dicen que nada ha mejorado desde mayo. Por ello, a principios de agosto, los habitantes de varias comunidades protestaron  y realizaron un paro tanto en el coliseo del cantón Joya de las Sachas como en los puntos de los derrames en el río Intillama exigiendo a Petroecuador que limpie el agua. </span>

[caption id="attachment_254058" align="alignnone" width="1600"]<img class="size-full wp-image-254058" src="https://imgs.mongabay.com/wp-content/uploads/sites/25/2024/08/30212151/Imagen-de-WhatsApp-2024-06-27-a-las-22.22.34_55a5fde1.jpg" alt="Comunicado del Ministerio de Ambiente sobre los derrames en Orellana." width="1600" height="1600" /> Comunicado del Ministerio de Ambiente sobre los derrames en Orellana.[/caption]

<span style="font-weight: 400;">Sus voces parecen ser ignoradas. También los llamados de las organizaciones ambientales y sociales que los respaldan. </span>

<span style="font-weight: 400;">A finales de julio, Amazon Frontlines, Acción Ecológica y tres organizaciones más difundieron un comunicado de prensa en el que destacan que los recientes derrames han afectado a más de 500 personas y a la cuenca del río Napo. “Los pescados del río saben a petróleo, los suelos de sus fincas están contaminados, sus cultivos de maíz, yuca y cacao están dañados y los niños se han enfermado debido a la contaminación de las fuentes de agua potable. Siguen sin agua para lavar su ropa, bañarse y tomar”. </span>

<span style="font-weight: 400;">Worsdell agrega que la empresa distribuyó agua por algunos días, pero luego se fueron y los derrames han llegado, por el río Napo, hasta la comunidad de Puerto Providencia, en el límite norte del Parque Nacional Yasuní. También aseguran que las granjas de pesca de las comunidades se contaminaron.</span>

<span style="font-weight: 400;">En el comunicado, las organizaciones también resaltan que la contaminación provocada por los derrames petroleros es un problema histórico que ha provocado más de 531 casos de cáncer en la región. Tan solo en el cantón Joya de los Sacha hasta diciembre de 2023 se habían documentado 119 casos.</span>

[caption id="attachment_254056" align="alignnone" width="738"]<img class="size-full wp-image-254056" src="https://imgs.mongabay.com/wp-content/uploads/sites/25/2024/08/30211653/WhatsApp-Image-2024-06-29-at-06.57.20.jpeg" alt="Contaminación petrolera en el río Shipati. Foto: comunidades locales." width="738" height="1600" /> Contaminación petrolera en el río Shipati. Foto: comunidades locales.[/caption]

<span style="font-weight: 400;">Pese a la gravedad de la situación, Petroecuador no entregaría beneficios porque los habitantes kichwa de las comunidades San Antonio y Joya de los Sachas en la parroquia Pompeya no cuentan con títulos de propiedad, pese a ser su territorio ancestral, aseguraron habitantes a las organizaciones “El gobierno tampoco da recursos para actualizar los tubos petroleros”, dice Worsdell. Por esta y otras razones, las organizaciones llamaron a que las entidades nacionales investiguen la situación.</span>

<span style="font-weight: 400;">“Hemos visto peces, caimanes y tapires muertos”, dice Leandro Tapuy, presidente de la comunidad Intillama, a Mongabay Latam. “Los políticos solo aparecen cada cinco años cuando necesitan votos”, agrega. </span>

&nbsp;

<span style="font-weight: 400;">Worsdell señala que en la zona hay un </span><i><span style="font-weight: 400;">tour</span></i><span style="font-weight: 400;"> turístico llamado “Toxitour”, donde los viajeros visitan sitios históricos de derrames petroleros y pasivos ambientales. “Por estos derrames y este modelo extractivista con sus desastres, deberíamos aplicar la consulta del Yasuní. Prometen la remediación y luego no cumplen”. Agrega que las medidas de remediación y de contingencia son artesanales, sin los implementos necesarios, no resuelven la situación a largo plazo y tampoco limpian el río cuyo corriente corre con los contaminantes.</span>

<span style="font-weight: 400;">Lucitante señala que  “estos derrames son recurrentes, siempre los hay. Las empresas tratan de ocultarlos, pero la situación se les salió de las manos recientemente y las comunidades kichwa están exigiendo soluciones”.</span>

<em><strong>*Imagen principal:</strong> </em>Múltiples derrames petroleros afectaron la provincia de Orellana de mayo a agosto de 2024. Foto: Amazon Frontlines.
<h3>_______</h3>
<h3>Lo más leído | <a href="https://es.mongabay.com/list/soluciones/" target="_blank" rel="noopener">Revisa nuestra cobertura periodística sobre soluciones ambientales</a></h3>
[iframe src="https://es.mongabay.com/2024/03/el-descubrimiento-del-misterioso-pudu-de-la-yunga-peruana-una-nueva-especie-que-habita-los-bosques-nubosos/embed/#?secret=nQfAAkIOhT" width="720" height="300" frameborder="0" data-secret="nQfAAkIOhT"&gt;&lt;/iframe]
<h3>Podcast Ambiental | <a href="https://es.mongabay.com/2024/02/crisis-climatica-iniciativas-que-luchan-contra-escasez-de-agua-dulce/">Esperanza en tiempo de crisis climática: cuatro iniciativas que luchan contra la inminente escasez de agua dulce</a></h3>
<em>Síguenos en nuestro canal de <a href="https://open.spotify.com/show/1TvMV7SIRbuNT22WVMeRI2" target="_blank" rel="noopener">Spotify</a> y encuentra más podcast sobre actualidad ambiental</em>

[iframe style="border-radius:12px" src="https://open.spotify.com/embed/episode/4wdqXBph3RXMLD4qcsXumO?utm_source=generator" width="100%" height="300" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"&gt;&lt;/iframe]
"""
cleaned_html = remove_span_tags(html_input)
print(cleaned_html)