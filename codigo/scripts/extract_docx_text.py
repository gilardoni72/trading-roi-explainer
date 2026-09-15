import zipfile
import xml.etree.ElementTree as ET

def extract_docx_text():
    docx_path = "C:/OpenCode/1-integracion-tbf/Inicio de Aplicacion- Demostracion.docx"
    output_path = "C:/OpenCode/1-integracion-tbf/codigo/database/temp_docx_text.txt"
    
    try:
        with zipfile.ZipFile(docx_path) as z:
            doc_xml = z.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            
            # El namespace para Word XML
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            paragraphs = []
            for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                texts = [node.text for node in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write('\n'.join(paragraphs))
                
            print(f"Texto extraído con éxito en: {output_path}")
    except Exception as e:
        print(f"Error extrayendo texto: {str(e)}")

if __name__ == "__main__":
    extract_docx_text()
