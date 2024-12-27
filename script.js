document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    // Mock resume data for chatbot
    const resumeData = {
        skills: ['Docker', 'Tensorflow', 'AWS', 'Flask'],
        
        certifications: ['Data Science certification by PW Skills', 'Intro to Data Engg. coursera']
    };

    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(sender);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleChatbotResponse(query) {
        // Simple rule-based chatbot logic
        query = query.toLowerCase();
        
        if (query.includes('skills')) {
            return `My key skills include: ${resumeData.skills.join(', ')}`;
        }
        if (query.includes('experience')) {
            return `I worked at ${resumeData.experience[0].company} as a ${resumeData.experience[0].role}`;
        }
        if (query.includes('certification')) {
            return `My certifications: ${resumeData.certifications.join(', ')}`;
        }
        
        return "I can help you with questions about my skills, experience, or certifications.";
    }

    sendBtn.addEventListener('click', () => {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            addMessage(userMessage, 'user');
            const botResponse = handleChatbotResponse(userMessage);
            setTimeout(() => addMessage(botResponse, 'bot'), 500);
            chatInput.value = '';
        }
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });
});