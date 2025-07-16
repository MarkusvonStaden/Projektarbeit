import { useEffect, useState, useCallback } from "react"; // Füge useCallback hinzu
import {
  Sidebar,
  SidebarBody,
  SidebarItem,
  SidebarSection,
  SidebarHeading,
  SidebarLabel,
} from "@/components/sidebar";
import { SidebarLayout } from "@/components/sidebar-layout";
import { ChatWindow } from "@/components/chat-window";
import { SidebarHeader } from "./components/sidebar";
import {

QuestionMarkCircleIcon,

PlusIcon,

InformationCircleIcon,

} from "@heroicons/react/20/solid";
import { Route, Routes } from "react-router-dom";
import { NewQuestion } from "@/components/new-question";
import { UserView, AdminView } from "@/components/views"

function Example() {
  const [userQuestions, setUserQuestions] = useState([]);
  const [adminQuestions, setAdminQuestions] = useState([]);
  const [activeItemId, setActiveItemId] = useState(null);

  // Verwende useCallback, um zu verhindern, dass fetchQuestions bei jedem Render neu erstellt wird
  const fetchQuestions = useCallback(async () => {
    try {
      const userResponse = await fetch("http://localhost/questions");
      const data = await userResponse.json();
      const withoutAnswer = data.filter((item) => !item.answer);
      console.log("Fetched questions:", data);
      console.log("Filtered unanswered questions:", withoutAnswer);
      setUserQuestions(data);
      setAdminQuestions(withoutAnswer);
    } catch (error) {
      console.error("Failed to fetch questions:", error);
    }
  }, []); // Leeres Abhängigkeits-Array, da keine externen Abhängigkeiten

  useEffect(() => {
    fetchQuestions();
  }, [fetchQuestions]); // fetchQuestions als Abhängigkeit, da es eine Callback-Funktion ist

  const handleItemClick = (id) => {
    setActiveItemId(id);
  };

  return (
    <SidebarLayout
      sidebar={
        <Sidebar>
          <SidebarHeader>
            <SidebarSection>
              <SidebarItem to="/">
                <PlusIcon />
                <SidebarLabel>New Question</SidebarLabel>
              </SidebarItem>
            </SidebarSection>
          </SidebarHeader>
          <SidebarBody>
            <SidebarSection>
              <SidebarHeading>User</SidebarHeading>
              {userQuestions.map((item) => (
                <SidebarItem
                  key={item.id}
                  to={`/user/${item.id}`}
                  onClick={() => handleItemClick(item.id)}
                  current={activeItemId === item.id ? "page" : undefined}
                >
                  <QuestionMarkCircleIcon />
                  <SidebarLabel>{item.question}</SidebarLabel>
                </SidebarItem>
              ))}
            </SidebarSection>
            <SidebarSection>
              <SidebarHeading>Admin</SidebarHeading>
              {adminQuestions.map((item) => (
                <SidebarItem
                  key={item.id}
                  to={`/admin/${item.id}`}
                  onClick={() => handleItemClick(item.id)}
                  current={activeItemId === item.id ? "page" : undefined}
                >
                  <InformationCircleIcon className="size-8" />
                  <SidebarLabel>{item.question}</SidebarLabel>
                </SidebarItem>
              ))}
            </SidebarSection>
          </SidebarBody>
        </Sidebar>
      }
    >
        <Routes>
          <Route path="/" element={<NewQuestion updateSidebar={fetchQuestions} />} />
          <Route path="/user/:id" element={<UserView updateSidebar={fetchQuestions} />} />
          <Route path="/admin/:id" element={<AdminView updateSidebar={fetchQuestions} />} />
        </Routes>
    </SidebarLayout>
  );
}

export default Example;