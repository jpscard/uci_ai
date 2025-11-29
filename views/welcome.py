# --- Importações Essenciais ---
import streamlit as st
import base64
import os

def welcome_screen():
    """Exibe a tela de boas-vindas com um design aprimorado e moderno para a Ucí AI."""

    # CSS para estilizar os cartões e a página
    st.markdown("""
    <style>
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 25px 20px;
        text-align: center;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        transition: 0.3s;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    .card h5 {
        color: #495057;
        font-size: 1.2rem;
        margin-bottom: 15px;
        text-align: center;
    }
    .card p {
        color: #6c757d;
        text-align: justify;
        font-size: 0.95rem;
    }
    .stButton>button {
        font-size: 1.1rem;
        padding: 10px 24px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Seção Hero ---
    with st.container():
        logo_path = "assets/img/LOGO.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(
                f"<div style='text-align: center; padding-bottom: 20px;'><img src='data:image/png;base64,{data}' width='300'></div>",
                unsafe_allow_html=True
            )
        
        st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Bem-vindo à Ucí AI</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #34495e; margin-bottom: 30px;'>Sua solução inteligente para análise de materiais recicláveis</h3>", unsafe_allow_html=True)

        _ , btn_col, _ = st.columns([2.5, 1.5, 2.5])
        with btn_col:
            if st.button("♻️ Iniciar Análise", width='stretch', type="primary"):
                st.session_state.welcome_seen = True
                st.rerun()

    st.markdown("--- ")

    # --- Seção de Funcionalidades ---
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Funcionalidades Principais</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <div style='font-size: 4rem;'>🤖</div>
            <h5>Detecção por IA</h5>
            <p>Utilize nosso modelo de Inteligência Artificial para detectar e classificar automaticamente materiais recicláveis como garrafas e latas em imagens e vídeos.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <div style='font-size: 4rem;'>📄</div>
            <h5>Relatórios Completos</h5>
            <p>Receba um relatório detalhado da análise, com a contagem de itens, gráficos e um cupom de desconto baseado nos materiais reciclados.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <div style='font-size: 4rem;'>🎥</div>
            <h5>Múltiplas Fontes</h5>
            <p>Analise mídias de diversas fontes, incluindo upload de imagens e vídeos, webcam em tempo real ou links do YouTube.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("--- ")

    # --- Seção ODS ---
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Contribuindo para um Futuro Sustentável</h2>", unsafe_allow_html=True)
    
    sdg_col1, sdg_col2, sdg_col3 = st.columns(3)
    with sdg_col1:
        st.markdown("""
        <div class="card">
            <img src="https://gtagenda2030.org.br/wp-content/uploads/2019/10/ods11.jpg" width="165">
            <h5>ODS 11: Cidades e Comunidades Sustentáveis</h5>
            <p>A Ucí AI contribui para a ODS 11 ao promover cidades mais limpas e sustentáveis. Nossa plataforma otimiza a gestão de resíduos sólidos, um serviço básico essencial para a qualidade de vida urbana. Ao facilitar a reciclagem, reduzimos a poluição, melhoramos a saúde pública e apoiamos a criação de assentamentos humanos mais seguros, resilientes e inclusivos para todos.</p>
        </div>
        """, unsafe_allow_html=True)
    with sdg_col2:
        st.markdown("""
        <div class="card">
            <img src="https://gtagenda2030.org.br/wp-content/uploads/2019/10/ods12.jpg" width="165">
            <h5>ODS 12: Consumo e Produção Responsáveis</h5>
            <p>A Ucí AI é uma ferramenta chave para a ODS 12, incentivando o consumo e a produção responsáveis. Ao transformar resíduos em recursos, nossa plataforma promove a economia circular e a gestão sustentável dos recursos naturais. Recompensar os usuários pelo descarte correto de recicláveis incentiva um estilo de vida mais sustentável e alinhado com os limites do nosso planeta.</p>
        </div>
        """, unsafe_allow_html=True)
    with sdg_col3:
        st.markdown("""
        <div class="card">
            <img src="https://gtagenda2030.org.br/wp-content/uploads/2019/10/ods17.jpg" width="165">
            <h5>ODS 17: Parcerias e Meios de Implementação</h5>
            <p>A Ucí AI promove a ODS 17 ao criar uma ponte entre tecnologia, sociedade e gestão de resíduos. Nossa plataforma fortalece a colaboração entre cidadãos, empresas e o poder público, utilizando dados para otimizar a coleta seletiva e incentivar a economia circular. Ao viabilizar parcerias multissetoriais, impulsionamos a inovação e a capacidade de implementação de soluções sustentáveis, revitalizando a parceria global para um desenvolvimento mais justo e ecológico.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("--- ")

    # --- Como Começar ---
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Como Começar</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
            <div style='font-size: 3.5rem; color: #0d6efd; font-weight: 600;'>1️⃣</div>
            <h5 style="margin-top: 15px;">Inicie a Análise</h5>
            <p>Clique no botão 'Iniciar Análise' para acessar a plataforma de detecção.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <div style='font-size: 3.5rem; color: #0d6efd; font-weight: 600;'>2️⃣</div>
            <h5 style="margin-top: 15px;">Escolha a Fonte</h5>
            <p>Selecione a aba correspondente à fonte de sua mídia: imagem, vídeo, webcam ou YouTube.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
            <div style='font-size: 3.5rem; color: #0d6efd; font-weight: 600;'>3️⃣</div>
            <h5 style="margin-top: 15px;">Receba seu Cupom</h5>
            <p>Após a análise, visualize o relatório, a pontuação e o cupom de desconto gerado para você.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- Seção da Equipe ---
    st.markdown("--- ")
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Nossa Equipe</h2>", unsafe_allow_html=True)

    # CSS para as imagens da equipe
    st.markdown("""
    <style>
    .team-member-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Membros da equipe
    team_members = [
        {"name": "Felipe Rafael dos Santos Barbosa", "email": "rafaelt.ibarbosa@gmail.com", "image": "assets/img/felipe.jpg"},
        {"name": "João Paulo da Silva Cardoso", "email": "jpscardoso@ufpa.br", "image": "assets/img/jpc.jpg"},
        {"name": "Victor Amazonas Viegas Ferreira", "email": "viegasdeveloper@gmail.com", "image": "assets/img/victor.png"}
    ]

    # Exibir membros da equipe em um grid
    cols = st.columns(3)
    for i, member in enumerate(team_members):
        with cols[i % 3]:
            image_path = member["image"]
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                image_html = f"<img class='team-member-img' src='data:image/png;base64,{data}'>"
            else:
                image_html = f"<img class='team-member-img' src='{image_path}'>"

            st.markdown(f"""
            <div class="card">
                {image_html}
                <h5>{member["name"]}</h5>
                <p>{member["email"]}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- Rodapé ---
    st.markdown("<p style='text-align: center; color: #7f8c8d; padding-top: 30px;'>Uma solução inteligente para um planeta mais limpo.</p>", unsafe_allow_html=True)
