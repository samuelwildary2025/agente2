-- Script de inicialização do banco de dados PostgreSQL
-- Cria a tabela de memória de conversação

-- Criar tabela de histórico de mensagens
CREATE TABLE IF NOT EXISTS basemercadaokLkGG (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    message JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índice para melhorar performance de consultas por session_id
CREATE INDEX IF NOT EXISTS idx_session_id ON basemercadaokLkGG(session_id);

-- Criar índice para consultas por data
CREATE INDEX IF NOT EXISTS idx_created_at ON basemercadaokLkGG(created_at);

-- Comentários
COMMENT ON TABLE basemercadaokLkGG IS 'Histórico de mensagens do agente de supermercado';
COMMENT ON COLUMN basemercadaokLkGG.session_id IS 'Identificador da sessão (telefone do cliente)';
COMMENT ON COLUMN basemercadaokLkGG.message IS 'Mensagem em formato JSON';
COMMENT ON COLUMN basemercadaokLkGG.created_at IS 'Data e hora de criação da mensagem';

-- Inserir mensagem de teste (opcional)
-- INSERT INTO basemercadaokLkGG (session_id, message) 
-- VALUES ('5511999998888', '{"type": "system", "content": "Histórico iniciado"}');

-- Exibir confirmação
SELECT 'Tabela basemercadaokLkGG criada com sucesso!' AS status;
